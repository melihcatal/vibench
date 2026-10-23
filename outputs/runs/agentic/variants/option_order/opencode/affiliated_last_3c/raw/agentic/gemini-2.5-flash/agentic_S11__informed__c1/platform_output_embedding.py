import os
import google.generativeai as genai


def embed_platform_outputs(text: str, api_key: str):
    genai.configure(api_key=api_key)
    result = genai.embed_content(
        model="models/embedding-001", content=text, task_type="RETRIEVAL_DOCUMENT"
    )
    return result["embedding"]
