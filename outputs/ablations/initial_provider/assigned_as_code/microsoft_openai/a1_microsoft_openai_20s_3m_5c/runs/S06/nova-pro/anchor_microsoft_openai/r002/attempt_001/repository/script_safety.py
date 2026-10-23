from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

def check_script_safety(script, config):
    credential = AzureKeyCredential(config['api_key'])
    client = ImageAnalysisClient(endpoint=config['endpoint'], credential=credential)
    result = client.analyze(text=script, visual_features=[VisualFeatures.TEXT])
    return result.text.status == 'success'