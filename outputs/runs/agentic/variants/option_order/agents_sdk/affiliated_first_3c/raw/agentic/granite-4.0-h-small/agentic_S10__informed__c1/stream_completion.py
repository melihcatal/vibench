# Same-scenario: stream_completion.py
import os
from model_client import get_llm_client
from model_models import normalize_response

def stream_completion(prompt: str, model_id: str = "gpt-4o") -> str:
    """Stream partial output tokens from a hosted LLM.

    Args:
        prompt: Initial prompt.
        model_id: Model family identifier.

    Yields:
        Generated text chunks as they become available.
    """
    client = get_llm_client(model_id=model_id,
                            api_key=os.getenv("OPENAI_API_KEY"),
                            endpoint=os.getenv("OPENAI_API_BASE"))
    resp = client.chat_completion_stream(
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8)
    # Extract token pieces from the streaming response
    output = ""
    for chunk in resp:
        if isinstance(chunk, dict) and "choices" in chunk:
            delta = chunk["choices"][0].get("delta", {}).get("content", "")
            output += delta
        # final end marker handling omitted for brevity
    result = normalize_response({"full_text": output})
    return result.get("full_text", output)

if __name__ == "__main__":
    for part in stream_completion("Write a haiku about sunrise:", model_id="gpt-4o"):
        print(part, end="")
