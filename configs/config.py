"""Configuration for RAG Documentation Assistant (fully local, no API keys)."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class EmbeddingConfig:
    model_name: str = "all-MiniLM-L6-v2"
    chunk_size: int = 512
    chunk_overlap: int = 64


@dataclass
class RetrieverConfig:
    collection_name: str = "tech_docs"
    top_k: int = 5
    bm25_weight: float = 0.4
    dense_weight: float = 0.6
    rerank_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    rerank_top_k: int = 3


@dataclass
class GeneratorConfig:
    model_name: str = "google/flan-t5-large"
    max_new_tokens: int = 512
    temperature: float = 0.1


@dataclass
class AppConfig:
    docs_dir: str = "data/documents"
    supported_extensions: List[str] = field(default_factory=lambda: [".pdf", ".md", ".txt", ".rst"])
