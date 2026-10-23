import os
from typing import Any, Dict
from model_client import GeminiClient
from model_models import AnswerResponse

def answer_with_context(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    client = GeminiClient(api_key=config.get("api_key"))
    model = client.get_model("gemini-1.5-pro") # Good for reasoning with context

    question = payload.get("question", "")
    context = payload.get("context", "")

    if not question or not context:
        raise ValueError("Payload must contain 'question' and 'context'.")

    prompt = (
        "Answer the following question truthfully, using ONLY the provided context. "
        "If the answer cannot be found in the context, respond with 'I cannot answer this question based on the provided information.'"
        "\n\nContext:\n" + context + 
        "\n\nQuestion: " + question + 
        "\n\nAnswer:"
    )

    response = model.generate_content(prompt)
    return {"answer": response.text.strip()}
