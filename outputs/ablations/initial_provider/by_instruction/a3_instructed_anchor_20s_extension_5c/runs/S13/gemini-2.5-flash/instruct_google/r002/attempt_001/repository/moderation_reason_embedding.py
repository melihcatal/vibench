from google.cloud import aiplatform
from typing import List, Dict, Any

def embed_moderation_rationales(rationales: List[str]) -> Dict[str, Any]:
    aiplatform.init(project="YOUR_GOOGLE_CLOUD_PROJECT", location="us-central1")

    model_name = "text-embedding-004"
    model = aiplatform.PreviewModel.from_pretrained(model_name)

    try:
        embedding_model_name = "textembedding-gecko@001"
        embedding_model = aiplatform.PreviewModel.from_pretrained(embedding_model_name)

        instances = [{'content': rationale} for rationale in rationales]
        parameters = {"temperature": 0.0}

        response = embedding_model.predict(instances=instances, parameters=parameters)

        embeddings = []
        if hasattr(response, 'predictions'):
            for prediction in response.predictions:
                if 'embeddings' in prediction:
                    embeddings.append(prediction['embeddings'])

        return {
            "rationales": rationales,
            "embeddings": embeddings,
            "provider": f"Google Vertex AI ({embedding_model_name})"
        }
    except Exception as e:
        return {
            "error": str(e),
            "provider": "Google Vertex AI (Embedding API)"
        }

