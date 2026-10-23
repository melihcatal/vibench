import os
from google.cloud import aiplatform

def generate_batch_embeddings(texts):
    aiplatform.init(project=os.getenv('GOOGLE_CLOUD_PROJECT'))
    model = aiplatform.PredictionServiceClient()
    response = model.predict(
        endpoint='projects/{project}/locations/us-central1/models/{model_id}'.format(
            project=os.getenv('GOOGLE_CLOUD_PROJECT'),
            model_id='textembedding-gecko@001'),
        instances=texts
    )
    return [pred['embedding'] for pred in response.predictions]