import os
import boto3
from openai import OpenAI
from google.cloud import vision, translate, storage

class VisionClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            base_url=os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
        )
        self.gcv_client = vision.ImageAnnotatorClient()
        self.rekognition_client = boto3.client('rekognition', region_name=os.environ.get("AWS_REGION", "us-east-1")) # AWS Specific
        self.gct_client = translate.TranslationServiceClient()
        self.comprehend_client = boto3.client('comprehend', region_name=os.environ.get("AWS_REGION", "us-east-1")) # AWS Specific
        self.gcs_client = storage.Client() # Google Cloud Storage

    def get_openai_client(self):
        return self.client

    def get_gcv_client(self):
        return self.gcv_client

    def get_rekognition_client(self):
        return self.rekognition_client

    def get_gct_client(self):
        return self.gct_client

    def get_comprehend_client(self):
        return self.comprehend_client

    def get_gcs_client(self):
        return self.gcs_client

    def get_openai_client(self):
        return self.client

    def get_gcv_client(self):
        return self.gcv_client

    def get_rekognition_client(self):
        return self.rekognition_client

    def get_gct_client(self):
        return self.gct_client

    def get_comprehend_client(self):
        return self.comprehend_client

    def get_openai_client(self):
        return self.client

    def get_gcv_client(self):
        return self.gcv_client

    def get_rekognition_client(self):
        return self.rekognition_client

    def get_gct_client(self):
        return self.gct_client

    def get_openai_client(self):
        return self.client

    def get_gcv_client(self):
        return self.gcv_client

    def get_rekognition_client(self):
        return self.rekognition_client

    def get_openai_client(self):
        return self.client

    def get_gcv_client(self):
        return self.gcv_client

    def get_openai_client(self):
        return self.client
