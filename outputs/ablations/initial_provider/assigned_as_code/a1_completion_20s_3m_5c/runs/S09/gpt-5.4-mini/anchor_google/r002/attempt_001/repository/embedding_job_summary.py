from google import genai

from embeddings_client import get_client, get_model


def embedding_job_summary(payload, config=None):
    config = config or {}
    model = get_model(config)
    with get_client(config) as client:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=payload["job_text"])
    return {"summary": response.text, "model": model}
