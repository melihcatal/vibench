import google.generativeai as genai
import os


def embed_output(text: str) -> list:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)
    result = genai.embed_content(
        model="models/embedding-001", content=text, task_type="RETRIEVAL_DOCUMENT"
    )
    return result["embedding"]
