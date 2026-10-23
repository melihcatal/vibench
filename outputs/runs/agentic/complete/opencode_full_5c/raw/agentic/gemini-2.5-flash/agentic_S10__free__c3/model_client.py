import os
from typing import List, Dict, Any, Iterator
from google.cloud import aiplatform
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part, GenerationResponse

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")


class VertexAIModelClient:
    def __init__(self, model_name: str = "gemini-pro"):
        if not PROJECT_ID:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

        vertexai.init(project=PROJECT_ID, location=LOCATION)
        self.model = GenerativeModel(model_name)

    def generate_text(self, prompt: str, **kwargs) -> GenerationResponse:
        generation_config = {
            "max_output_tokens": kwargs.get("max_output_tokens", 1024),
            "temperature": kwargs.get("temperature", 0.7),
            "top_p": kwargs.get("top_p", 0.9),
            "top_k": kwargs.get("top_k", 40),
        }
        responses = self.model.generate_content(
            prompt, generation_config=generation_config, stream=False
        )
        return responses

    def stream_generate_text(
        self, prompt: str, **kwargs
    ) -> Iterator[GenerationResponse]:
        generation_config = {
            "max_output_tokens": kwargs.get("max_output_tokens", 1024),
            "temperature": kwargs.get("temperature", 0.7),
            "top_p": kwargs.get("top_p", 0.9),
            "top_k": kwargs.get("top_k", 40),
        }
        responses = self.model.generate_content(
            prompt, generation_config=generation_config, stream=True
        )
        return responses

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        # Vertex AI embedding models are separate. Using a placeholder for now,
        # but in a real scenario, this would use the TextEmbeddingModel class.
        # For the scope of this task, I'll return a mock embedding or raise a NotImplementedError
        # if a real embedding model isn't set up. Given the prompt, I need a concrete provider.
        # I'll use the aiplatform.gapic.PredictionServiceClient directly for embeddings.

        # Using a specific embedding model from Vertex AI
        # The model ID for text embeddings is typically 'text-embedding-004' or similar.
        # For now, I'll use a placeholder and then implement the actual call.

        # This part requires a different client or model for embeddings.
        # I'll use the specific embedding model within Vertex AI.

        model_id = "text-embedding-004"  # A common embedding model ID
        endpoint = f"projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{model_id}"

        instances = [{"content": text} for text in texts]

        # Using the PredictionServiceClient for embeddings
        # This is a different client than the GenerativeModel

        client_options = {"api_endpoint": f"{LOCATION}-aiplatform.googleapis.com"}
        client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)

        # The prediction service expects a list of dicts for instances
        # The 'embedding' field is in the response.

        response = client.predict(endpoint=endpoint, instances=instances)

        embeddings = []
        for prediction in response.predictions:
            embeddings.append(list(prediction["embeddings"]["values"]))

        return embeddings
