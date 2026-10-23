import os
import boto3
from google.cloud import aiplatform
from openai import AzureOpenAI
import cohere

class AWSBedrockClient:
    def __init__(self):
        self.client = boto3.client(
            service_name='bedrock-runtime',
            region_name=os.environ.get('AWS_REGION', 'us-east-1')
        )

class GCPVertexAIClient:
    def __init__(self):
        project_id = os.environ.get('GCP_PROJECT_ID')
        location = os.environ.get('GCP_LOCATION', 'us-central1')
        aiplatform.init(project=project_id, location=location)
        self.client = aiplatform.predict.PredictionServiceClient.from_service_account_json(
            os.environ.get('GCP_SA_KEY_PATH')
        )
        self.project_id = project_id
        self.location = location

class AzureOpenAIClient:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
            api_version="2024-02-01",
            azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT")
        )

class CohereClient:
    def __init__(self):
        self.client = cohere.Client(os.environ.get("COHERE_API_KEY"))

# You can add more client configurations here as needed.
