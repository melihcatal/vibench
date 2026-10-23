from google import genai

from embeddings_client import DEFAULT_GEMINI_EMBED_MODEL, get_google_client


def embedding_job_summary(job_text: str) -> str:
    client = get_google_client()
    prompt = f"Summarize this embedding job result in one concise sentence: {job_text}"
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    return response.text
