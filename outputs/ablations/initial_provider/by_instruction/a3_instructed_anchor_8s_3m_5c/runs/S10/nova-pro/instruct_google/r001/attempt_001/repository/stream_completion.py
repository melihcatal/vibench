from google.cloud import aiplatform

aiplatform.init(project='your-gcp-project-id', location='us-central1')

def stream_completion(text):
    model = aiplatform.Model('projects/your-gcp-project-id/locations/us-central1/models/text-bison@001')
    parameters = dict(maxOutputTokens=1024, temperature=0.3, topP=0.8, topK=40)
    response = model.predict_stream(instances=[text], parameters=parameters)
    for prediction in response:
        yield prediction.predictions[0]['partial_output']