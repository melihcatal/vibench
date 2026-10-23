import os
import boto3
from google.cloud import vision
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential
from clarifai.client.image import Image as ClarifaiImage # Not strictly a client, but used for input
from clarifai.client.workflow import Workflow # Used for Clarifai scored file

class VisionClients:
    """Provides initialized clients for various vision services."""

    @staticmethod
    def get_google_vision_client():
        """Returns a Google Cloud Vision ImageAnnotatorClient."""
        # GOOGLE_APPLICATION_CREDENTIALS should be set
        return vision.ImageAnnotatorClient()

    @staticmethod
    def get_azure_vision_client():
        """Returns an Azure AI Vision ImageAnalysisClient."""
        endpoint = os.environ.get("AZURE_VISION_ENDPOINT")
        key = os.environ.get("AZURE_VISION_KEY")
        if not endpoint or not key:
            raise ValueError("AZURE_VISION_ENDPOINT and AZURE_VISION_KEY must be set for Azure AI Vision.")
        return ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    @staticmethod
    def get_aws_rekognition_client():
        """Returns an Amazon Rekognition client."""
        region = os.environ.get("AWS_REGION", "us-east-1")
        # AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY should be set
        return boto3.client("rekognition", region_name=region)

    @staticmethod
    def get_clarifai_workflow(workflow_id: str):
        """Returns a Clarifai Workflow object."""
        pat = os.environ.get("CLARIFAI_PAT")
        if not pat:
            raise ValueError("CLARIFAI_PAT must be set for Clarifai.")
        return Workflow(workflow_id=workflow_id, pat=pat)

if __name__ == '__main__':
    # Example usage (requires env vars to be set)
    # try:
    #     google_client = VisionClients.get_google_vision_client()
    #     print("Google Vision client initialized.")
    # except Exception as e:
    #     print(f"Google Vision client failed: {e}")

    # try:
    #     azure_client = VisionClients.get_azure_vision_client()
    #     print("Azure Vision client initialized.")
    # except Exception as e:
    #     print(f"Azure Vision client failed: {e}")

    # try:
    #     aws_client = VisionClients.get_aws_rekognition_client()
    #     print("AWS Rekognition client initialized.")
    # except Exception as e:
    #     print(f"AWS Rekognition client failed: {e}")

    # try:
    #     clarifai_workflow = VisionClients.get_clarifai_workflow("moderation-workflow")
    #     print("Clarifai workflow initialized.")
    # except Exception as e:
    #     print(f"Clarifai workflow failed: {e}")
    pass
