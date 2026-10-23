from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import ImageAnalysisMode
from azure.core.credentials import AzureKeyCredential

def extract_key_values(image_path):
    client = ImageAnalysisClient(endpoint="https://<your-resource-name>.cognitiveservices.azure.com/", credential=AzureKeyCredential("<your-api-key>"))
    with open(image_path, "rb") as image_data:
        result = client.analyze(image_data, visual_features=[ImageAnalysisMode.LAYOUT])
        return result.layout.key_value_pairs if result.layout and result.layout.key_value_pairs else ""