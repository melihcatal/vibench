import os
import google.generativeai as genai


def embed_caption_chunk(text: str) -> list[float]:
    # GOOGLE_API_KEY environment variable is expected to be set
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    try:
        response = genai.embed_content(
            model="models/embedding-001", content=text, task_type="RETRIEVAL_DOCUMENT"
        )
        return response["embedding"]
    except Exception as e:
        print(f"Error embedding content: {e}")
        return []
