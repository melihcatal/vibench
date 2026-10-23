import os
from model_client import get_llm_client
from model_models import InferenceResponse

def summarize_text(text: str, model_family: str = "gpt-4") -> str:
    """Summarize long text using a hosted LLM.

    Args:
        text: The input text to summarize.
        model_family: Identifier for the LLM family/model (default: "gpt-4").

    Returns:
        A concise summary of the input text.
    """
    client = get_llm_client(model_family)
    payload = {
        "model": model_family,
        "prompt": f"Summarize the following text in no more than 3 sentences:\n\n{text}",
        "temperature": 0.3,
    }
    response = client.chat_completion(payload)  # type: ignore
    # Assume response contains a field 'choices' with generated text
    summary = response.choices[0].message.content
    return summary
