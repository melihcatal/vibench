import os
import requests
from auth0.management import Auth0
from dotenv import load_dotenv

load_dotenv()


class Auth0Client:
    def __init__(self):
        self.domain = os.getenv("AUTH0_DOMAIN")
        self.management_client_id = os.getenv("AUTH0_MANAGEMENT_CLIENT_ID")
        self.management_client_secret = os.getenv("AUTH0_MANAGEMENT_CLIENT_SECRET")
        self.audience = os.getenv("AUTH0_AUDIENCE")
        self.client_id = os.getenv("AUTH0_CLIENT_ID")
        self.auth0_management = self._get_management_client()

    def _get_management_client(self):
        if (
            not self.domain
            or not self.management_client_id
            or not self.management_client_secret
        ):
            raise ValueError(
                "Auth0 management credentials are not fully configured in environment variables."
            )

        # First, get a management API token
        token_url = f"https://{self.domain}/oauth/token"
        payload = {
            "client_id": self.management_client_id,
            "client_secret": self.management_client_secret,
            "audience": f"https://{self.domain}/api/v2/",
            "grant_type": "client_credentials",
        }

        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(token_url, json=payload, headers=headers)
            response.raise_for_status()
            access_token = response.json().get("access_token")
            return Auth0(self.domain, access_token)
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to get Auth0 Management API token: {e}")

    def get_management_api_client(self):
        return self.auth0_management

    def get_auth_api_url(self, path: str):
        if not self.domain:
            raise ValueError("AUTH0_DOMAIN is not set in environment variables.")
        return f"https://{self.domain}{path}"


class DeepLClient:
    def __init__(self):
        self.auth_key = os.getenv("DEEPL_AUTH_KEY")
        if not self.auth_key:
            raise ValueError("DEEPL_AUTH_KEY is not set in environment variables.")
        self.api_url = "https://api-free.deepl.com/v2/translate"  # Or https://api.deepl.com for Pro

    def translate_text(
        self, text: str, target_lang: str, source_lang: Optional[str] = None
    ):
        headers = {
            "Authorization": f"DeepL-Auth-Key {self.auth_key}",
            "Content-Type": "application/json",
        }
        payload = {"text": [text], "target_lang": target_lang.upper()}
        if source_lang:
            payload["source_lang"] = source_lang.upper()

        response = requests.post(self.api_url, headers=headers, json=payload)
        response.raise_for_status()
        translations = response.json().get("translations", [])
        return translations[0]["text"] if translations else ""


class AzureContentSafetyClient:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
        if not self.endpoint or not self.key:
            raise ValueError(
                "AZURE_CONTENT_SAFETY_ENDPOINT or AZURE_CONTENT_SAFETY_KEY is not set."
            )
        self.api_version = "2023-10-01"

    def moderate_text(self, text: str):
        url = (
            f"{self.endpoint}/contentsafety/text:analyze?api-version={self.api_version}"
        )
        headers = {
            "Ocp-Apim-Subscription-Key": self.key,
            "Content-Type": "application/json",
        }
        payload = {
            "text": text,
            "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
            "blocklists": [],
            "breakByBlocklists": False,
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()


class AnthropicClient:
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY is not set in environment variables.")
        self.api_url = "https://api.anthropic.com/v1/messages"
        self.headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        self.model = "claude-3-haiku-20240307"  # Using a specific Anthropic model

    def create_message(
        self, system_prompt: str, user_message: str, max_tokens: int = 1000
    ):
        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_message}],
        }
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()


class MongoDBClient:
    def __init__(self):
        self.mongo_uri = os.getenv("MONGODB_ATLAS_URI")
        if not self.mongo_uri:
            raise ValueError("MONGODB_ATLAS_URI is not set in environment variables.")
        from pymongo import MongoClient

        self.client = MongoClient(self.mongo_uri)
        self.db = self.client.get_database("onboarding_notes")  # Default database

    def get_collection(self, collection_name: str):
        return self.db.get_collection(collection_name)
