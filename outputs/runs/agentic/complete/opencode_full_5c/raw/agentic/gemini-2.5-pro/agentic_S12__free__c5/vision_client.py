import os
import boto3
import cohere
import openai
from google.cloud import vision
from google.cloud import translate_v2 as translate
from googleapiclient import discovery


def get_vision_client():
    return vision.ImageAnnotatorClient()


def get_openai_client():
    return openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def get_cohere_client():
    return cohere.Client(os.environ.get("COHERE_API_KEY"))


def get_translate_client():
    return translate.Client()


def get_perspective_client():
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    return discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )


def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
    )
