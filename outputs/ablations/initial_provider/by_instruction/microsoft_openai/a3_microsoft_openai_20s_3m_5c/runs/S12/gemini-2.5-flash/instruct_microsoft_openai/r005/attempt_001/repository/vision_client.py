import os
from openai import OpenAI
from google.cloud import vision_v1p3beta1 as vision
from google.cloud import translate_v2 as translate
from azure.cognitiveservices.contentmoderator import ContentModeratorClient
import msrest.authentication
import boto3

class VisionClient:
    def __init__(self):
        # OpenAI Client
        self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.openai_vision_model_id = os.environ.get("OPENAI_VISION_MODEL_ID", "gpt-4o")
        self.openai_text_model_id = os.environ.get("OPENAI_TEXT_MODEL_ID", "gpt-3.5-turbo")

        # Google Cloud Vision Client
        self.google_vision_client = vision.ImageAnnotatorClient()

        # Google Cloud Translation Client
        self.google_translate_client = translate.Client()

        # Azure Content Moderator Client
        self.azure_content_moderator_key = os.environ.get("AZURE_CONTENT_MODERATOR_KEY")
        self.azure_content_moderator_endpoint = os.environ.get("AZURE_CONTENT_MODERATOR_ENDPOINT")
        if self.azure_content_moderator_key and self.azure_content_moderator_endpoint:
            self.azure_content_moderator_client = ContentModeratorClient(
                endpoint=self.azure_content_moderator_endpoint,
                credentials=msrest.authentication.CognitiveServicesCredentials(self.azure_content_moderator_key)
            )
        else:
            self.azure_content_moderator_client = None

        # AWS S3 Client
        self.aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
        self.aws_region_name = os.environ.get("AWS_REGION_NAME", "us-east-1")
        if self.aws_access_key_id and self.aws_secret_access_key:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.aws_region_name
            )
        else:
            self.s3_client = None

    def get_openai_client(self):
        return self.openai_client

    def get_openai_vision_model_id(self):
        return self.openai_vision_model_id
    
    def get_openai_text_model_id(self):
        return self.openai_text_model_id

    def get_google_vision_client(self):
        return self.google_vision_client

    def get_google_translate_client(self):
        return self.google_translate_client

    def get_azure_content_moderator_client(self):
        if not self.azure_content_moderator_client:
            raise RuntimeError("Azure Content Moderator client not initialized. Check AZURE_CONTENT_MODERATOR_KEY and AZURE_CONTENT_MODERATOR_ENDPOINT environment variables.")
        return self.azure_content_moderator_client

    def get_s3_client(self):
        if not self.s3_client:
            raise RuntimeError("AWS S3 client not initialized. Check AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.")
        return self.s3_client

    def get_aws_s3_bucket_name(self):
        return os.environ.get("AWS_S3_BUCKET_NAME")