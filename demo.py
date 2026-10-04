"""RAG Demo - runs entirely locally, no API keys needed."""

exec(open("create_sample_docs.py").read())

from src.pipeline import RAGPipeline

pipeline = RAGPipeline()
n = pipeline.build_index("data/documents")
print(f"\nIndexed {n} chunks. Ready!\n")

questions = [
    "How does authentication work in the API?",
    "What are the prerequisites for deployment?",
    "How do the microservices communicate with each other?",
    "What happens when the rate limit is exceeded?",
    "How is security handled between services?",
]

for q in questions:
    print(f"\n{'='*60}")
    print(f"Q: {q}")
    print(f"{'='*60}")
    result = pipeline.query(q)
    print(f"\nA: {result['answer']}\n")
    print("Sources:")
    for s in result["sources"]:
        print(f"  - {s['source_file']} (chunk {s['chunk_id']}, score: {s['relevance_score']:.3f})")
