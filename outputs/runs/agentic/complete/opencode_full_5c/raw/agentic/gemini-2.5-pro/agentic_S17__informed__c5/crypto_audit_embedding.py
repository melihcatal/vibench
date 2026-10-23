import os
import openai


def embed_crypto_audit_note(note_text: str) -> list[float]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    # Provider-specific client initialization
    client = openai.OpenAI(api_key=api_key)

    # Provider-specific model ID
    model_id = "text-embedding-3-small"

    response = client.embeddings.create(input=note_text, model=model_id)

    return response.data[0].embedding
