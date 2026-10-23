from google.cloud import aiplatform

aiplatform.init(project='your-gcp-project-id', location='us-central1')

def answer_with_context(question, context):
    model = aiplatform.Model('projects/your-gcp-project-id/locations/us-central1/models/text-bison@001')
    parameters = dict(maxOutputTokens=1024, temperature=0.3, topP=0.8, topK=40)
    response = model.predict(instances=[question + ' ' + context], parameters=parameters)
    return response.predictions[0]['answer']