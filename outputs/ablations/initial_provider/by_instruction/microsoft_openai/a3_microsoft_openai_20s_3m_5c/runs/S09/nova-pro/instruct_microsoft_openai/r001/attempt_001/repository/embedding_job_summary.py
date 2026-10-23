from embeddings_client import EmbeddingsClient

client = EmbeddingsClient()

job_results = [{'id': '1', 'status': 'completed'}, {'id': '2', 'status': 'failed'}]

summary = {result['id']: result['status'] for result in job_results}

print(summary)