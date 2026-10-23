from google.cloud import aiplatform

def platform_output_embedding(text_content: str, project_id: str, location: str):
    aiplatform.init(project=project_id, location=location)
    
    # Using the 'textembedding-gecko@003' model for embeddings
    # Ensure this model is available in your specified project and location
    model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
    
    embeddings = model.get_embeddings([text_content])
    
    return {"embedding": embeddings[0].values}
