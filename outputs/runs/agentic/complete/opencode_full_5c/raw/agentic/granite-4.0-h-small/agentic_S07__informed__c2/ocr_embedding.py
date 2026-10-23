from google.cloud import genai


def ocr_embedding(text, model="textembedding-gecko@001"):
    """Embed extracted document sections for semantic retrieval using Gemini embeddings."""
    client = genai.Client()
    embed = client.embed_content(model, parts=[genai.Part(content=text)])
    return embed[0].embedding
