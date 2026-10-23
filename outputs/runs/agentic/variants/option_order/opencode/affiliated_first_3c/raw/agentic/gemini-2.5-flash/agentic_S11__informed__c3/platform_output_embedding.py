import os
import google.generativeai as genai


def platform_output_embedding(text: str) -> list[float]:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = "models/embedding-001"
    response = genai.embed_content(model=model, content=text)
    return response["embedding"]
