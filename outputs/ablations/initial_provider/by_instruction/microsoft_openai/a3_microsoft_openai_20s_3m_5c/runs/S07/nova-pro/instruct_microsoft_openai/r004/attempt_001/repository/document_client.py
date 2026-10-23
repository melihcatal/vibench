import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import ImageAnalysisOptions, TextDocumentAnalysisOptions, TextDocumentFeatures, TableDocumentFeatures
from azure.core.credentials import AzureKeyCredential

class DocumentClient:
    def __init__(self, endpoint, key):
        self.endpoint = endpoint
        self.key = key
        self.client = ImageAnalysisClient(endpoint, AzureKeyCredential(key))

    def analyze_document(self, image_path, features):
        with open(image_path, "rb") as image_data:
            options = ImageAnalysisOptions(text_document_analysis_options=TextDocumentAnalysisOptions(features=features))
            result = self.client.analyze(image_data, options)
            return result
