import os
import base64
from typing import Dict, Any
from openai import OpenAI
from google.cloud import vision_v1 as vision
from google.cloud import translate_v2 as translate
import google.generativeai as genai
import boto3

openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
vision_client = vision.ImageAnnotatorClient()
translate_client = translate.Client()
genai.configure(api_key=os.getenv('GOOGLE_GENAI_API_KEY'))
gemini_model = genai.GenerativeModel('gemini-1.5-flash')
s3_client = boto3.client('s3', region_name=os.getenv('AWS_REGION', 'us-east-1'))

def image_to_base64(image_path: str) -> str:
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def get_image_mime(image_path: str) -> str:
    ext = os.path.splitext(image_path)[1].lower()
    mime_map = {'.jpg': 'jpeg', '.jpeg': 'jpeg', '.png': 'png', '.gif': 'gif'}
    return f"image/{mime_map.get(ext, 'jpeg')}"
