import os
import google.generativeai as genai


def embed_script(text: str) -> list[float]:
    # GOOGLE_API_KEY environment variable should be set
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = "models/embedding-001"
    response = genai.embed_content(model=model, content=text)
    return response["embedding"]
