import os
from google.cloud import aiplatform

def embed_for_search(query, documents):
    aiplatform.init(project=os.getenv('GOOGLE_CLOUD_PROJECT'))
    model = aiplatform.PredictionServiceClient()
    query_embedding = model.predict(
        endpoint='projects/{project}/locations/us-central1/models/{model_id}'.format(
            project=os.getenv('GOOGLE_CLOUD_PROJECT'),
            model_id='textembedding-gecko@001'),
        instances=[query]
    ).predictions[0]['embedding']
    document_embeddings = model.predict(
        endpoint='projects/{project}/locations/us-central1/models/{model_id}'.format(
            project=os.getenv('GOOGLE_CLOUD_PROJECT'),
            model_id='textembedding-gecko@001'),
        instances=documents
    ).predictions
    return query_embedding, [pred['embedding'] for pred in document_embeddings]