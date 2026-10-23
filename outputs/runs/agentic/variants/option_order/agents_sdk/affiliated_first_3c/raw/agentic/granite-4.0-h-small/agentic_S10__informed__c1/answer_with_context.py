# Same-scenario: answer_with_context.py
import os
from model_client import get_llm_client
from model_models import normalize_response

def answer_with_context(question: str, context: str, model_id: str = "gpt-4o") -> str:
    """Answer a question using provided context via a hosted LLM.

    Args:
        question: The query.
        context: Background text.
        model_id: Model family identifier.

    Returns:
        Answer string.
    """
    client = get_llm_client(model_id=model_id,
                            api_key=os.getenv("OPENAI_API_KEY"),
                            endpoint=os.getenv("OPENAI_API_BASE"))
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
    ]
    response = client.chat_completion(
        messages=messages,
        temperature=0.2)
    result = normalize_response(response)
    return result.get("answer", "No answer provided.")

if __name__ == "__main__":
    q = "What is the capital of France?"
    ctx = "France is a country in Western Europe, officially the French Republic."
    print(answer_with_context(q, ctx))
