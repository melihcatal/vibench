from model_client import GeminiClient
from model_models import ModelPayload, ModelResponse

def get_output_embedding(payload: ModelPayload) -> ModelResponse:
    client = GeminiClient()
    model = client.get_embedding_model(model_name="embedding-001")
    
    # The embedding model expects a list of texts
    result = model.embed_content(contents=[payload.text])
    
    embeddings = []
    if result.embeddings:
        for embedding_obj in result.embeddings:
            embeddings.extend(embedding_obj.values)
            
    return ModelResponse(text=payload.text, embeddings=embeddings)
