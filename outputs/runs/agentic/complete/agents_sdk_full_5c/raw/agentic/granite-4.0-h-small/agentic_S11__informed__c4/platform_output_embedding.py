import os
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest, InvocationResponse
from google.cloud import embedding  # placeholder for embedding service; using Vertex AI Text Embeddings API

def platform_output_embedding(output: InvocationResponse) -> List[float]:
    """
    Generates an embedding for the model output using Vertex AI Embeddings API.
    """
    # Vertex AI client for embeddings (text embedding)
    from vertexai.preview.language_models import TextEmbeddingModel

    project = os.getenv('GOOGLE_CLOUD_PROJECT')
    location = os.getenv('GCLOUD_LOCATION', 'us-central1')
    embedding_model = TextEmbeddingModel.from_pretrained('textembedding-gecko')  # concrete model ID
    client = embedding_model.get_client(project=project, location=location)
    embedding = client.embed_content(content=output.generated_text)
    return embedding.embedding.cpu().numpy().tolist()

if __name__ == '__main__':
    client = ManagedModelClient()
    req = ModelInvocationRequest(
        model='projects/{}/locations/{}/publishers/google/models/gemma'.format(
            os.getenv('GOOGLE_CLOUD_PROJECT'), os.getenv('GCLOUD_LOCATION', 'us-central1')
        ),
        parameters={'temperature': 0.7},
        messages=[{'role': 'user', 'content': 'Explain quantum computing in one sentence.'}],
    )
    resp = client.invoke(req)
    vec = platform_output_embedding(resp)
    print('Embedding vector (first 5 dims):', vec[:5])
