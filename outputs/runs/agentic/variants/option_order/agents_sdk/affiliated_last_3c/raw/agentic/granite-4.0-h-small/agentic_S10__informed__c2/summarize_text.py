import os
import json
from model_client import get_llm_client
from model_models import LLMRequest, LLMResponse

def summarize_text(text: str, model_family: str = "gpt-4") -> str:
    """Summarize long text using a hosted LLM.

    Args:
        text (str): The input text to summarize.
        model_family (str): Identifier for the LLM model family.

    Returns:
        str: The summarized text.
    """
    client = get_llm_client(model_family)
    request = LLMRequest(
        prompt=f"Summarize the following text in no more than 150 words:\n\n{text}",
        model=model_family,
        temperature=0.3,
        max_tokens=256,
    )
    response = client.chat_completion(request)
    # ensure response is string
    return str(response.choices[0].message.content)

if __name__ == "__main__":
    sample = """Python is a high-level, interpreted programming language known for its clear syntax and..."""
    print(summarize_text(sample, model_family="gpt-4"))