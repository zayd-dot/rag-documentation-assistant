# RAG Documentation Assistant

A retrieval-augmented generation application for natural-language questions over technical documentation. It combines hybrid retrieval, cross-encoder reranking, and local Flan-T5 generation, returning answers alongside retrieved source metadata.

## Pipeline

1. Load PDF, Markdown, TXT, or RST documents.
2. Split documents into overlapping text chunks.
3. Index chunks with BM25 and MiniLM embeddings in ChromaDB.
4. Retrieve keyword and semantic matches.
5. Merge rankings with weighted reciprocal rank fusion.
6. Rerank candidate passages with a cross-encoder.
7. Generate an answer from the top three passages.

## Components

| Component | Configuration |
|---|---|
| Chunking | Recursive character splitting; 512 characters, 64-character overlap |
| Embeddings | `all-MiniLM-L6-v2` |
| Keyword retrieval | BM25 |
| Vector search | ChromaDB with cosine similarity |
| Rank fusion | BM25 weight 0.4, dense weight 0.6 |
| Reranker | `cross-encoder/ms-marco-MiniLM-L-6-v2` |
| Generation | `google/flan-t5-large` |
| Answer context | Top three reranked chunks |
| Source metadata | Filename, page where available, chunk ID, relevance score |

The models run locally after their files are downloaded. The application does not require a paid language-model API key.

## Output

Each query returns generated answer text, retrieved source records, the number of context chunks, and the generator model name. The prompt requests inline source references. An interactive CLI supports multiple questions within one session.

## Quick Start

```bash
python -m pip install -r requirements.txt
python demo.py
```

Place your documents in `data/documents/`, then run:

```bash
python main.py --docs-dir data/documents query "How does the system handle errors?"
python main.py --docs-dir data/documents interactive
```

## Project Structure

| File | Purpose |
|---|---|
| `src/ingestion.py` | Document loading and chunking |
| `src/retriever.py` | Hybrid search, rank fusion, and reranking |
| `src/generator.py` | Answer generation and source metadata |
| `src/pipeline.py` | End-to-end orchestration |
| `main.py` | Query and interactive CLI |
| `demo.py` | Sample-document demonstration |
| `configs/config.py` | Model and retrieval settings |

## Technologies

Python, Transformers, SentenceTransformers, LangChain document utilities, ChromaDB, BM25, and PyTorch.
