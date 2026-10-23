from google.cloud import aiplatform
from document_client import get_vertex_ai_model_garden_client
from document_models import DocumentConfig, EmbeddingResult


def ocr_embedding(texts: list[str], config: DocumentConfig) -> EmbeddingResult:
    # Initialize Vertex AI
    aiplatform_client = get_vertex_ai_model_garden_client(config.project_id, config.location)

    # For text embeddings, we use a pre-trained text embedding model from Vertex AI.
    # The 'text-embedding-gecko@001' is a common choice.
    
    try:
        # Ensure the model is available and deployed
        # You can specify a different model_id in config if needed.
        model_id = config.model_id if config.model_id else "text-embedding-gecko@001"
        model = aiplatform.get_model(f"publishers/google/models/{model_id}")
        
        # Prepare instances for prediction
        instances = [{'content': text} for text in texts]
        
        # Make a prediction request
        response = model.predict(instances=instances)
        
        embeddings_list = []
        if response.predictions:
            for prediction in response.predictions:
                # Assuming the prediction directly contains the embedding vector
                # The structure might vary based on the specific embedding model
                if 'embeddings' in prediction and 'values' in prediction['embeddings']:
                    embeddings_list.append(prediction['embeddings']['values'])
                else:
                    print(f"Warning: Unexpected prediction format: {prediction}")

        return EmbeddingResult(embeddings=embeddings_list)
    except Exception as e:
        print(f"Error during embedding generation: {e}")
        return EmbeddingResult(embeddings=[])
