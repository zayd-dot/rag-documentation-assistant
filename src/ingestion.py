"""Document loading, chunking, and ingestion."""

import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from configs.config import EmbeddingConfig, AppConfig

LOADER_MAP = {
    ".pdf": PyPDFLoader,
    ".md": UnstructuredMarkdownLoader,
    ".txt": TextLoader,
    ".rst": TextLoader,
}


def load_documents(docs_dir: str, extensions: List[str]) -> List[Document]:
    documents = []
    for root, _, files in os.walk(docs_dir):
        for fname in sorted(files):
            ext = os.path.splitext(fname)[1].lower()
            if ext not in extensions:
                continue
            fpath = os.path.join(root, fname)
            loader_cls = LOADER_MAP.get(ext)
            if loader_cls is None:
                continue
            try:
                docs = loader_cls(fpath).load()
                for doc in docs:
                    doc.metadata["source_file"] = fname
                    doc.metadata["file_path"] = fpath
                documents.extend(docs)
                print(f"  Loaded: {fname} ({len(docs)} pages/sections)")
            except Exception as e:
                print(f"  Error loading {fname}: {e}")
    print(f"Total documents loaded: {len(documents)}")
    return documents


def chunk_documents(documents: List[Document], cfg: EmbeddingConfig = EmbeddingConfig()) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=cfg.chunk_size, chunk_overlap=cfg.chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(documents)
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i
    print(f"Created {len(chunks)} chunks (size={cfg.chunk_size}, overlap={cfg.chunk_overlap})")
    return chunks


def ingest(docs_dir=None, cfg_app=AppConfig(), cfg_emb=EmbeddingConfig()):
    directory = docs_dir or cfg_app.docs_dir
    print(f"Ingesting documents from '{directory}'...")
    documents = load_documents(directory, cfg_app.supported_extensions)
    return chunk_documents(documents, cfg_emb)
