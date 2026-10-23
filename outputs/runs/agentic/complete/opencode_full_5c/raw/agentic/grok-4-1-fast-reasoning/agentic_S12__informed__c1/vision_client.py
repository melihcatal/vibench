import os
from typing import List

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential

def get_azure_vision_client() -&gt; ImageAnalysisClient:
    endpoint = os.environ[&quot;AZURE_VISION_ENDPOINT&quot;]
    key = os.environ[&quot;AZURE_VISION_KEY&quot;]
    return ImageAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )