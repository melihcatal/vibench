from typing import Any, Dict
from google.cloud import aiplatform


def extract_document_fields(normalized_text: str) -> Dict[str, Any]:
    endpoint = aiplatform.Endpoint(endpoint_name=os.environ['VERTEX_AI_ENDPOINT_NAME'])
    prediction = endpoint.predict(instances=[{'content': normalized_text}], parameters={})
    return {'provider': 'vertex_ai', 'predictions': prediction.predictions}
