"""Answer generation using local HuggingFace model (no API key needed)."""

from typing import List, Tuple, Dict, Any
from langchain_core.documents import Document
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

from configs.config import GeneratorConfig


class RAGGenerator:
    def __init__(self, cfg: GeneratorConfig = GeneratorConfig()):
        self.cfg = cfg
        print(f"Loading {cfg.model_name}...")
        self.tokenizer = AutoTokenizer.from_pretrained(cfg.model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = AutoModelForSeq2SeqLM.from_pretrained(cfg.model_name).to(self.device)
        print(f"Model loaded on {self.device.upper()}")
        self.conversation_history = []

    def _generate(self, prompt, max_tokens=512):
        inputs = self.tokenizer(prompt, return_tensors="pt", max_length=1024, truncation=True).to(self.device)
        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=max_tokens, temperature=0.1, do_sample=False)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def generate(self, query, retrieved, use_history=True):
        context_parts, sources = [], []
        for i, (doc, score) in enumerate(retrieved):
            source_file = doc.metadata.get("source_file", "unknown")
            page = doc.metadata.get("page", "N/A")
            chunk_id = doc.metadata.get("chunk_id", i)
            context_parts.append(f"[Source {i+1}]: {doc.page_content}")
            sources.append({
                "source_file": source_file, "page": page,
                "chunk_id": chunk_id, "relevance_score": round(score, 4),
                "preview": doc.page_content[:150] + "...",
            })

        context = "\n\n".join(context_parts)
        prompt = (
            f"Answer the question based on the context. Cite sources using [Source N].\n\n"
            f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer:"
        )

        answer = self._generate(prompt, self.cfg.max_new_tokens)
        self.conversation_history.append({"query": query, "answer": answer})

        return {
            "answer": answer, "sources": sources,
            "context_used": len(retrieved), "model": self.cfg.model_name,
        }

    def clear_history(self):
        self.conversation_history = []
