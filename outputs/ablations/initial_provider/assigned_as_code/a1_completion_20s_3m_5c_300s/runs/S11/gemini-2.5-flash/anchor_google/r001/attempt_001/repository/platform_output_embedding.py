from google import genai

def platform_output_embedding(text: str, project_id: str, location: str):
    with genai.Client(vertexai=True, project=project_id, location=location) as client:
        # Using an embedding model, for example, 'text-embedding-004'
        embedding_model = client.get_model("text-embedding-004")
        response = embedding_model.embed_content(content=text)
    
    embedding = []
    if response.embedding: 
        embedding = response.embedding.values

    return {"text": text, "embedding": embedding}
