from typing import List, Dict
from model_client import get_cohere_client

def answer_with_context(question: str, context_docs: List[Dict[str, str]]) -> str:
    """
    Answers a question using a provided list of context documents (RAG).
    """
    client = get_cohere_client()

    # The chat endpoint's `documents` parameter enables Retrieval-Augmented Generation
    response = client.chat(
        model="command-r",
        question=question,
        documents=context_docs,
        prompt_truncation='AUTO'
    )

    return response.answer
