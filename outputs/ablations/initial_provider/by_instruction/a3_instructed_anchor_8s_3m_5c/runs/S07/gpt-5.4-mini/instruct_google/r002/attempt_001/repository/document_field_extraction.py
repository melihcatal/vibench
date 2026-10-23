from google.cloud import aiplatform

from document_models import normalize_text


def extract_document_fields(text: str, project: str, location: str, model_name: str):
    aiplatform.init(project=project, location=location)
    model = aiplatform.Model(model_name)
    response = model.predict(instances=[{"text": normalize_text(text)}])
    return response.predictions
