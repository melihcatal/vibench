import openai
from model_client import get_openai_client

def answer_with_context(question: str, context: str, model: str = "gpt-4o-mini") -> str:
    """Answer a question using provided context via OpenAI GPT model.
\n    Args:\n        question: The query to answer.\n        context: Background text for the model.\n        model: Model identifier (default gpt-4o-mini).\n    Returns:\n        Answer string.\n    """
    client = get_openai_client()
    response = client.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an assistant that answers questions using only the provided context."},
            {"role": "user", "content": f"Given the context:\n\n{context}\n\\nAnswer the question:\n\\n{question}"}],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()
