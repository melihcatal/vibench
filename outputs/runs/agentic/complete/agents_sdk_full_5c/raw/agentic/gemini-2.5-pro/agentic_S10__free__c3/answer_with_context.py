from model_client import get_cohere_client
from typing import List

def answer_with_context(question: str, context_documents: List[dict]) -> str:
    """
    Answers a question using a provided context (documents) with Cohere's RAG capabilities.

    Args:
        question: The user's question.
        context_documents: A list of documents, where each document is a dict with a 'text' key.

    Returns:
        The answer generated from the context.
    """
    cohere_client = get_cohere_client()

    # Provider-specific model ID: command-r
    response = cohere_client.chat(
        question=question,
        documents=context_documents,
        model='command-r',
        prompt_truncation='AUTO'
    )
    
    return response.answer
