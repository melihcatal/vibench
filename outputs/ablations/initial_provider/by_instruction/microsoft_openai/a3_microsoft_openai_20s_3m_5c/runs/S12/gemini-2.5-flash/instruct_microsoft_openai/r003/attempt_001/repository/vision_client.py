import os
from openai import OpenAI
from google.cloud import vision, videointelligence_v1 as videointelligence
import boto3

class VisionClient:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.google_vision_client = vision.ImageAnnotatorClient()
        self.google_video_intelligence_client = videointelligence.VideoIntelligenceServiceClient()
        self.aws_textract_client = boto3.client("textract", region_name=os.environ.get("AWS_REGION"))

    def get_openai_client(self):
        return self.openai_client

    def get_google_vision_client(self):
        return self.google_vision_client
        
    def get_google_video_intelligence_client(self):
        return self.google_video_intelligence_client

    def get_aws_textract_client(self):
        return self.aws_textract_client
