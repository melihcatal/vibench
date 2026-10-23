import os
import google.generativeai as genai


def embed_moderation_reason(reason_text: str) -> list[float]:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    model = "models/embedding-001"
    response = genai.embed_content(
        model=model, content=reason_text, task_type="RETRIEVAL_DOCUMENT"
    )

    return response["embedding"]
