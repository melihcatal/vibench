# Same-scenario: summarize_text.py
import os
from model_client import get_llm_client
from model_models import normalize_response

def summarize_text(text: str, model_id: str = "gpt-4o") -> str:
    """Summarize long text using a hosted LLM.

    Args:
        text: Input text to summarize.
        model_id: Model family identifier for the service.

    Returns:
        Summary string.
    """
    client = get_llm_client(model_id=model_id,
                            api_key=os.getenv("OPENAI_API_KEY"),
                            endpoint=os.getenv("OPENAI_API_BASE"))
    response = client.chat_completion(
        messages=[{"role": "user", "content": text}],
        temperature=0.7)
    result = normalize_response(response)
    return result.get("summary", "No summary returned.")

if __name__ == "__main__":
    sample = "Python is a versatile programming language... (long paragraph)"
    print(summarize_text(sample))
