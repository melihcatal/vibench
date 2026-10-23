import os

from google import genai


def embedding_job_summary(payload, config=None):
    config = config or {}
    api_key = config.get("api_key") or os.environ["GOOGLE_API_KEY"]
    model = config.get("model") or "gemini-embedding-001"
    summary_text = payload["summary_text"]
    with genai.Client(api_key=api_key) as client:
        response = client.models.embed_content(model=model, contents=summary_text)
    return {"embedding": list(response.embeddings[0].values)}
