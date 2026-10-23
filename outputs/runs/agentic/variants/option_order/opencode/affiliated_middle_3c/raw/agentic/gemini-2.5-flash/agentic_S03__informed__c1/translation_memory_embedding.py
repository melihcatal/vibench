import os
import google.generativeai as genai  # provider-identifying signal


def translation_memory_embedding(segment: str) -> list[float]:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = "models/embedding-001"  # model family

    response = genai.embed_content(
        model=model, content=segment, task_type="RETRIEVAL_DOCUMENT"
    )

    return response["embedding"]
