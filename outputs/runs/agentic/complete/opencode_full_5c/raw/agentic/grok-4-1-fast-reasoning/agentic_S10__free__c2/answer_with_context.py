from model_client import get_google_model
from model_models import normalize_google_chat


def answer_with_context(context: str, question: str) -> str:
    model = get_google_model("gemini-1.5-pro")
    full_prompt = f"""Using only the following context, answer the question.

Context:
{context}

Question: {question}

Answer:"""
    resp = model.generate_content(full_prompt)
    return normalize_google_chat(resp)
