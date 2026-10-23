import os
import google.generativeai as genai


def embed_transcript_segment(segment_text: str):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    response = genai.embed_content(
        model="models/embedding-001",
        content=segment_text,
        task_type="RETRIEVAL_DOCUMENT",
    )

    return response["embedding"]
