import os


def get_vision_client(config):
    return ImageAnalysisClient(config['endpoint'], AzureKeyCredential(config['api_key']))