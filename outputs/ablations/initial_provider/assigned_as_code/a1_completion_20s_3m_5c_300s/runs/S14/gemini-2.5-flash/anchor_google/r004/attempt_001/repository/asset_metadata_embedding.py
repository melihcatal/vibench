import os
import google.generativeai as genai

def asset_metadata_embedding(payload: dict) -> dict:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('text-embedding-004')
    
    # The text to embed can be a combination of metadata and extracted text.
    text_to_embed = payload["text"]

    response = model.embed_content(model="models/text-embedding-004", content=text_to_embed)

    if response.embedding and response.embedding.values:
        return {"embedding": response.embedding.values}
    else:
        return {"embedding": []}
