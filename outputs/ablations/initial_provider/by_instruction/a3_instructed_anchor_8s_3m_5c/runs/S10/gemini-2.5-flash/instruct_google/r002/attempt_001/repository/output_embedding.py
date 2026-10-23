import os
from google.cloud import aiplatform
from google.generativeai import GenerativeModel, configure

def get_embedding(text: str) -> list[float]:
    """
    Generates an embedding for the given text using a Google embedding model.
    """
    # For Vertex AI embedding model
    # aiplatform.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"), location=os.environ.get("GOOGLE_CLOUD_LOCATION"))
    # model = aiplatform.gapic.PredictionServiceClient(client_options={"api_endpoint": "us-central1-aiplatform.googleapis.com"})
    # instance = aiplatform.gapic.PredictRequest.Instance(struct_value={"text_embedding_input": {"text": text}})
    # endpoint = f"projects/{os.environ.get("GOOGLE_CLOUD_PROJECT")}/locations/{os.environ.get("GOOGLE_CLOUD_LOCATION")}/endpoints/text-embedding-garden"
    # response = model.predict(endpoint=endpoint, instances=[instance])
    # return list(response.predictions[0]['embeddings'])

    # For Gemini API (using a generative model for conceptual embedding, actual embedding model is preferred)
    # configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = GenerativeModel(model_name="gemini-pro") # Using gemini-pro as a placeholder for embedding, actual embedding model is `text-embedding-004` or similar
    response = model.embed_content(content=text)
    return response['embedding']
