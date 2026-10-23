import os
import google.generativeai as genai


def embed_platform_outputs(text: str) -> list[float]:
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set.")

    genai.configure(api_key=google_api_key)

    # Use a specific Gemini embedding model
    model = "models/embedding-001"

    response = genai.embed_content(model=model, content=text)
    return response["embedding"]
