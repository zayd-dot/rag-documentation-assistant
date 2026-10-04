"""End-to-end RAG pipeline."""
from typing import Dict, Any, Optional
from configs.config import EmbeddingConfig, RetrieverConfig, GeneratorConfig
from src.ingestion import ingest
from src.retriever import HybridRetriever
from src.generator import RAGGenerator


class RAGPipeline:
    def __init__(self, cfg_emb=EmbeddingConfig(), cfg_ret=RetrieverConfig(), cfg_gen=GeneratorConfig()):
        self.cfg_emb = cfg_emb
        self.retriever = HybridRetriever(cfg_emb, cfg_ret)
        self.generator = RAGGenerator(cfg_gen)
        self._indexed = False

    def build_index(self, docs_dir=None):
        chunks = ingest(docs_dir=docs_dir, cfg_emb=self.cfg_emb)
        self.retriever.index(chunks)
        self._indexed = True
        return len(chunks)

    def query(self, question, top_k=5):
        if not self._indexed:
            raise RuntimeError("Call build_index() first.")
        retrieved = self.retriever.retrieve(question, top_k=top_k)
        return self.generator.generate(question, retrieved)

    def clear_memory(self):
        self.generator.clear_history()
