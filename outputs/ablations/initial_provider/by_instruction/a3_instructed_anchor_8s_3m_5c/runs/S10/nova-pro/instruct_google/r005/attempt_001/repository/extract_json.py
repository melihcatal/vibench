import os
from google.cloud import aiplatform

def extract_json(text):
    aiplatform.init(project=os.getenv('GOOGLE_CLOUD_PROJECT'))
    model = aiplatform.PredictionServiceClient()
    response = model.predict(
        endpoint='projects/{project}/locations/{location}/publishers/google/models/text-bison@001'.format(
            project=os.getenv('GOOGLE_CLOUD_PROJECT'), location=os.getenv('GOOGLE_CLOUD_LOCATION')),
        instances=[{'content': text}]
    )
    return response.predictions[0]['content']