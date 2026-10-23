import os
import google.generativeai as genai


def transcript_embedding(text_segments, config=None):
    config = config or {}
    genai.configure(api_key=config.get('api_key') or os.environ.get('GEMINI_API_KEY'))

    model = genai.GenerativeModel('embedding-001')

    embeddings = []
    for segment in text_segments:
        response = model.embed_content(content=segment)
        embeddings.append(response['embedding'])

    return {"embeddings": embeddings, "provider": "Google Cloud Generative AI (embedding-001)"}
