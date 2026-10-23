from openai import OpenAI
from embeddings_client import embedding_model
from embeddings_models import embeddings_to_vectors


def embedding_job_summary(job_results):
    client = OpenAI()
    vectors = embeddings_to_vectors(client.embeddings.create(model=embedding_model(), input=[r['text'] for r in job_results]))
    total = len(vectors)
    dims = len(vectors[0]) if vectors else 0
    return {'provider': 'openai', 'model': embedding_model(), 'items': total, 'dimensions': dims}
