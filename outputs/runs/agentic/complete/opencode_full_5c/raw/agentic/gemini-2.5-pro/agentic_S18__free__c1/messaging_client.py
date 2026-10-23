import os
import boto3
from google.cloud import pubsub_v1, translate_v2 as translate
from googleapiclient import discovery
import openai


def get_pubsub_publisher_client():
    return pubsub_v1.PublisherClient()


def get_pubsub_subscriber_client():
    return pubsub_v1.SubscriberClient()


def get_dynamodb_resource():
    return boto3.resource(
        "dynamodb",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )


def get_translation_client():
    return translate.Client()


def get_perspective_client():
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    return discovery.build("commentanalyzer", "v1alpha1", developerKey=api_key)


def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    return openai.OpenAI(api_key=api_key)
