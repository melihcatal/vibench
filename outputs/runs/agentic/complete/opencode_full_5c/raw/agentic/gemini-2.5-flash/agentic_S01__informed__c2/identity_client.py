import os
from dotenv import load_dotenv
import requests
from google.cloud import translate_v2 as translate
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
import google.generativeai as genai
from google.cloud import firestore

load_dotenv()


class Auth0Client:
    def __init__(self):
        self.domain = os.getenv("AUTH0_DOMAIN")
        self.client_id = os.getenv("AUTH0_CLIENT_ID")
        self.client_secret = os.getenv("AUTH0_CLIENT_SECRET")
        self.audience = os.getenv("AUTH0_AUDIENCE")

        if not all([self.domain, self.client_id, self.client_secret, self.audience]):
            raise ValueError(
                "AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, and AUTH0_AUDIENCE must be set in environment variables"
            )

        self.management_api_url = f"https://{self.domain}/api/v2/"
        self.oauth_url = f"https://{self.domain}/oauth/token"
        self.passwordless_url = f"https://{self.domain}/dbconnections/change_password"

    def get_management_api_token(self):
        # In a real application, you'd cache this token and refresh it as needed.
        token_payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "audience": self.management_api_url,
            "grant_type": "client_credentials",
        }
        headers = {"content-type": "application/json"}
        response = requests.post(self.oauth_url, json=token_payload, headers=headers)
        response.raise_for_status()
        return response.json()["access_token"]

    def _management_api_headers(self):
        token = self.get_management_api_token()
        return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    def get_auth_headers(self):
        return {"Content-Type": "application/json"}


class GoogleTranslateClient:
    def __init__(self):
        # GOOGLE_APPLICATION_CREDENTIALS should be set in environment variables
        self.client = translate.Client()


class AzureContentSafetyClient:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
        if not all([self.endpoint, self.key]):
            raise ValueError(
                "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set in environment variables"
            )
        self.client = ContentSafetyClient(self.endpoint, AzureKeyCredential(self.key))


class GoogleGeminiClient:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY must be set in environment variables")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-pro")


class GoogleFirestoreClient:
    def __init__(self):
        # GOOGLE_APPLICATION_CREDENTIALS should be set in environment variables
        self.db = firestore.Client()
