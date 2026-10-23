from typing import List
from model_client import client

def answer_question_with_context(question: str, context_docs: List[str]) -> str:
    """
    Calls the Cohere API to answer a question given a set of context documents.
    This is a form of Retrieval-Augmented Generation (RAG).
    """
    documents = [{"title": f"doc_{i}", "snippet": doc} for i, doc in enumerate(context_docs)]
    
    response = client.chat(
        message=question,
        documents=documents,
        model="command-r",
        prompt_truncation='AUTO'
    )
    
    return response.text
