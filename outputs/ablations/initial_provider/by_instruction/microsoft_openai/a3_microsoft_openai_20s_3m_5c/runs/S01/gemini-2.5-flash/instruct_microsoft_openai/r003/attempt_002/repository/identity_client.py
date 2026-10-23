import os
from openai import AzureOpenAI
from auth0.management import Auth0
from google.cloud import translate_v2 as translate
from azure.cognitiveservices.contentmoderator import ContentModeratorClient
from azure.cognitiveservices.contentmoderator.models import ScreenTextOptionalInput
import boto3
from pymongo import MongoClient


class IdentityClient:
    def __init__(self):
        # OpenAI/Azure OpenAI Configuration
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        self.openai_api_base = os.environ.get("OPENAI_API_BASE")  # For Azure OpenAI
        self.openai_api_version = os.environ.get("OPENAI_API_VERSION", "2023-05-15")  # For Azure OpenAI
        self.openai_deployment_name = os.environ.get("OPENAI_DEPLOYMENT_NAME", "gpt-4")  # For Azure OpenAI

        if self.openai_api_key and self.openai_api_base:
            self.openai_client = AzureOpenAI(
                api_key=self.openai_api_key,
                api_version=self.openai_api_version,
                azure_endpoint=self.openai_api_base
            )
        elif self.openai_api_key:
            from openai import OpenAI
            self.openai_client = OpenAI(api_key=self.openai_api_key)
        else:
            self.openai_client = None

        # Auth0 Configuration
        self.auth0_domain = os.environ.get("AUTH0_DOMAIN")
        self.auth0_client_id = os.environ.get("AUTH0_CLIENT_ID")
        self.auth0_client_secret = os.environ.get("AUTH0_CLIENT_SECRET")
        self.auth0_audience = os.environ.get("AUTH0_AUDIENCE")

        if self.auth0_domain and self.auth0_client_id and self.auth0_client_secret and self.auth0_audience:
            # For machine-to-machine applications, you'd typically get a management API token.
            # For user login, you'd interact with the Auth0 '/oauth/token' endpoint directly.
            # This client focuses on administrative tasks if needed, or demonstrates endpoint interaction.
            self.auth0_management_client = Auth0(
                self.auth0_domain,
                self.auth0_client_id,
                self.auth0_client_secret
            )
            # Placeholder for direct OAuth client for user login/refresh
            self.auth0_oauth_base_url = f"https://{self.auth0_domain}"
        else:
            self.auth0_management_client = None
            self.auth0_oauth_base_url = None

        # Google Cloud Translation Configuration
        self.google_translation_client = translate.Client() # Assumes GOOGLE_APPLICATION_CREDENTIALS is set

        # Azure Content Moderator Configuration
        self.azure_content_moderator_key = os.environ.get("AZURE_CONTENT_MODERATOR_KEY")
        self.azure_content_moderator_endpoint = os.environ.get("AZURE_CONTENT_MODERATOR_ENDPOINT")

        if self.azure_content_moderator_key and self.azure_content_moderator_endpoint:
            self.azure_content_moderator_client = ContentModeratorClient(
                self.azure_content_moderator_endpoint, self.azure_content_moderator_key
            )
        else:
            self.azure_content_moderator_client = None

        # AWS Comprehend Configuration
        self.aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
        self.aws_region_name = os.environ.get("AWS_REGION_NAME", "us-east-1")

        if self.aws_access_key_id and self.aws_secret_access_key:
            self.aws_comprehend_client = boto3.client(
                "comprehend",
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.aws_region_name
            )
        else:
            self.aws_comprehend_client = None

        # MongoDB Atlas Configuration
        self.mongodb_uri = os.environ.get("MONGODB_URI")
        self.mongodb_database_name = os.environ.get("MONGODB_DATABASE_NAME", "identity_notes")
        self.mongodb_collection_name = os.environ.get("MONGODB_COLLECTION_NAME", "profile_notes")

        if self.mongodb_uri:
            try:
                self.mongodb_client = MongoClient(self.mongodb_uri)
                self.mongodb_db = self.mongodb_client[self.mongodb_database_name]
                self.mongodb_collection = self.mongodb_db[self.mongodb_collection_name]
            except Exception as e:
                print(f"Error connecting to MongoDB Atlas: {e}")
                self.mongodb_client = None
                self.mongodb_db = None
                self.mongodb_collection = None
        else:
            self.mongodb_client = None
            self.mongodb_db = None
            self.mongodb_collection = None
