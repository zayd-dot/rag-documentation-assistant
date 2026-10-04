"""Hybrid retrieval: BM25 + dense + cross-encoder re-ranking."""

import numpy as np
from typing import List, Tuple, Optional
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer, CrossEncoder
from langchain_core.documents import Document
import chromadb
from configs.config import EmbeddingConfig, RetrieverConfig


class HybridRetriever:
    def __init__(self, cfg_emb=EmbeddingConfig(), cfg_ret=RetrieverConfig()):
        self.cfg_ret = cfg_ret
        self.embedder = SentenceTransformer(cfg_emb.model_name)
        self.reranker = CrossEncoder(cfg_ret.rerank_model)
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(
            name=cfg_ret.collection_name, metadata={"hnsw:space": "cosine"},
        )
        self.documents: List[Document] = []
        self.bm25: Optional[BM25Okapi] = None

    def index(self, chunks: List[Document]) -> None:
        self.documents = chunks
        texts = [c.page_content for c in chunks]
        self.bm25 = BM25Okapi([t.lower().split() for t in texts])
        embeddings = self.embedder.encode(texts, show_progress_bar=True, batch_size=64)

        batch = 5000
        for s in range(0, len(chunks), batch):
            e = min(s + batch, len(chunks))
            self.collection.add(
                ids=[str(i) for i in range(s, e)],
                embeddings=embeddings[s:e].tolist(),
                documents=texts[s:e],
                metadatas=[c.metadata for c in chunks[s:e]],
            )
        print(f"Indexed {len(chunks)} chunks into BM25 + ChromaDB")

    def retrieve(self, query: str, top_k=None) -> List[Tuple[Document, float]]:
        top_k = top_k or self.cfg_ret.top_k

        bm25_scores = self.bm25.get_scores(query.lower().split())
        bm25_top = np.argsort(bm25_scores)[::-1][:top_k * 2]

        query_emb = self.embedder.encode(query).tolist()
        dense = self.collection.query(query_embeddings=[query_emb], n_results=top_k * 2)
        dense_top = [int(i) for i in dense["ids"][0]]

        fused = self._rrf(bm25_top.tolist(), dense_top,
                          self.cfg_ret.bm25_weight, self.cfg_ret.dense_weight)
        candidates = [(self.documents[i], i) for i in list(fused.keys())[:top_k * 2]
                       if i < len(self.documents)]
        if not candidates:
            return []

        pairs = [(query, doc.page_content) for doc, _ in candidates]
        scores = self.reranker.predict(pairs)
        scored = sorted([(candidates[i][0], float(scores[i])) for i in range(len(candidates))],
                        key=lambda x: x[1], reverse=True)
        return scored[:self.cfg_ret.rerank_top_k]

    @staticmethod
    def _rrf(bm25_idx, dense_idx, bm25_w=0.4, dense_w=0.6, k=60):
        scores = {}
        for r, i in enumerate(bm25_idx):
            scores[i] = scores.get(i, 0) + bm25_w / (k + r + 1)
        for r, i in enumerate(dense_idx):
            scores[i] = scores.get(i, 0) + dense_w / (k + r + 1)
        return dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
