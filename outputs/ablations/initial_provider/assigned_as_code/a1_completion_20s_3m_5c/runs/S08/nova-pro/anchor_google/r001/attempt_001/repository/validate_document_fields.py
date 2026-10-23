from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials


def validate_document_fields(document):
    client = ComputerVisionClient("https://westus2.api.cognitive.microsoft.com/", CognitiveServicesCredentials("YOUR_API_KEY"))
    read_results = client.read_in_stream(document['document_bytes'], raw=True)
    if not read_results.text:
        raise ValueError('No text detected in the document')
    required_fields = ['vendor', 'date', 'total']
    for field in required_fields:
        if field not in document:
            raise ValueError(f'Required field {field} is missing')
        if not document[field]:
            raise ValueError(f'Field {field} is empty')
    return True