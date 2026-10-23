import os
import google.generativeai as genai

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)


def embed_moderation_rationales(rationales: list[str]):
    model = "models/embedding-001"
    response = genai.embed_content(model=model, content=rationales)
    return [embedding.values for embedding in response["embedding"]]
