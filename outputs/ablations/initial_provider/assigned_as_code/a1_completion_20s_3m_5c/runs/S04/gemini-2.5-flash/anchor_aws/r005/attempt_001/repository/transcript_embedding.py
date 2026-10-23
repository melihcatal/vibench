from speech_client import get_vertex_ai_embedding_model

def transcript_embedding(payload: dict, config: dict = None):
    config = config or {}
    model_name = config.get("model_name", "text-embedding-004")
    model = get_vertex_ai_embedding_model(model_name)
    
    # The Vertex AI embedding model expects a list of texts
    segments_to_embed = payload["segments"]
    
    embeddings = []
    if segments_to_embed:
        # Ensure segments_to_embed is a list of strings
        if isinstance(segments_to_embed, str):
            segments_to_embed = [segments_to_embed]
        elif not isinstance(segments_to_embed, list):
            raise ValueError("Payload 'segments' must be a string or a list of strings.")

        response = model.get_embeddings(segments_to_embed)
        for embedding_obj in response:
            embeddings.append(embedding_obj.values)
    
    return {"embeddings": embeddings}
