from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import ImageAnalysisMode
from azure.core.credentials import AzureKeyCredential

def extract_fields(text):
    client = ImageAnalysisClient(endpoint="https://<your-resource-name>.cognitiveservices.azure.com/", credential=AzureKeyCredential("<your-api-key>"))
    result = client.analyze(text, visual_features=[ImageAnalysisMode.LAYOUT])
    return result.layout.fields if result.layout and result.layout.fields else ""