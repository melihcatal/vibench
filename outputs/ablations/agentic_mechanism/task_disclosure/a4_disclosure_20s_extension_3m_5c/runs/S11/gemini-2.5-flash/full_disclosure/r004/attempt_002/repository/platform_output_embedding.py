import google.generativeai as genai
import os

def embed_platform_output(text: str) -> list[float]:
    """
    Embeds platform outputs for evaluation or retrieval using Google's Generative AI.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.get_model("models/text-embedding-004")
    response = model.embed_content(content=text)
    return response["embedding"]
