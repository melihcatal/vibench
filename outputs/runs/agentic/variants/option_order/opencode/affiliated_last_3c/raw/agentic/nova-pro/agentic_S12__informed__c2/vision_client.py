import os


def get_vision_client():
    return ImageAnalysisClient(
        os.getenv("AZURE_VISION_ENDPOINT"),
        AzureKeyCredential(os.getenv("AZURE_VISION_KEY")),
    )


def get_vision_key():
    return os.getenv("AZURE_VISION_KEY")
