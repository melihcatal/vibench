import os
from openai import OpenAI
import boto3
from google.cloud import monitoring_v3, translate_v2 as translate, storage
import datadog

class ObservabilityClient:
    def __init__(self):
        # OpenAI Client
        self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        # AWS Clients
        self.aws_region = os.environ.get("AWS_REGION", "us-east-1")
        self.cloudwatch_client = boto3.client("cloudwatch", region_name=self.aws_region)
        self.comprehend_client = boto3.client("comprehend", region_name=self.aws_region)
        self.s3_client = boto3.client("s3", region_name=self.aws_region)

        # Google Cloud Clients
        self.google_project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
        self.monitoring_client = monitoring_v3.MetricServiceClient()
        self.translate_client = translate.Client()
        self.storage_client = storage.Client(project=self.google_project_id)

        # Datadog Client
        datadog.initialize(
            api_key=os.environ.get("DATADOG_API_KEY"),
            app_key=os.environ.get("DATADOG_APP_KEY")
        )
