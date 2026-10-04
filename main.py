"""CLI for the RAG Documentation Assistant.

Usage:
    python main.py index --docs-dir data/documents
    python main.py query "How does the system handle errors?"
    python main.py interactive
"""

import argparse
from src.pipeline import RAGPipeline


def cmd_query(args):
    pipeline = RAGPipeline()
    pipeline.build_index(args.docs_dir)
    result = pipeline.query(args.question, top_k=args.top_k)

    print(f"\n{'='*60}")
    print(f"Question: {args.question}")
    print(f"{'='*60}")
    print(f"\n{result['answer']}\n")
    print(f"{'='*60}")
    print(f"Sources ({result['context_used']} chunks used):")
    for s in result["sources"]:
        print(f"  - {s['source_file']} (page {s['page']}, score: {s['relevance_score']:.3f})")


def cmd_interactive(args):
    pipeline = RAGPipeline()
    pipeline.build_index(args.docs_dir)
    print("\nRAG Documentation Assistant (type 'quit' to exit, 'clear' to reset memory)\n")

    while True:
        question = input("You: ").strip()
        if question.lower() in ("quit", "exit"):
            break
        if question.lower() == "clear":
            pipeline.clear_memory()
            print("Memory cleared.\n")
            continue
        if not question:
            continue

        result = pipeline.query(question)
        print(f"\nAssistant: {result['answer']}\n")
        for s in result["sources"]:
            print(f"  📎 {s['source_file']} (page {s['page']})")
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RAG Documentation Assistant")
    parser.add_argument("--docs-dir", default="data/documents")
    sub = parser.add_subparsers(dest="command")

    p_q = sub.add_parser("query")
    p_q.add_argument("question", type=str)
    p_q.add_argument("--top-k", type=int, default=5)

    sub.add_parser("interactive")

    args = parser.parse_args()
    if args.command == "query":
        cmd_query(args)
    elif args.command == "interactive":
        cmd_interactive(args)
    else:
        parser.print_help()
