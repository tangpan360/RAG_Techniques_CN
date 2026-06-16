from __future__ import annotations

from typing import List


def retrieve_context_per_question(question: str, chunks_query_retriever) -> List[str]:
    """
    Retrieve relevant context for a question using a retriever.

    Notes:
    - Compatible with current LangChain retrievers via `.invoke(question)`.
    - Returns a list of chunk texts (strings).
    """
    docs = chunks_query_retriever.invoke(question)
    return [d.page_content for d in docs]


def show_context(context: List[str]) -> None:
    """Pretty-print a list of context strings."""
    for i, c in enumerate(context, start=1):
        print(f"Context {i}:")
        print(c)
        print()

