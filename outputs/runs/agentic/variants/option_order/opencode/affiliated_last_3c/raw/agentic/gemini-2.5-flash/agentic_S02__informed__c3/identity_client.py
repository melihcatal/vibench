import os
from typing import Optional
from identity_models import (
    Auth0Config,
    GoogleGeminiConfig,
    AzureContentSafetyConfig,
    DeepLConfig,
    FirestoreConfig,
)


def get_auth0_config() -> Auth0Config:
    return Auth0Config(
        domain=os.environ.get("AUTH0_DOMAIN", ""),
        client_id=os.environ.get("AUTH0_CLIENT_ID", ""),
        client_secret=os.environ.get("AUTH0_CLIENT_SECRET"),
        redirect_uri=os.environ.get("AUTH0_REDIRECT_URI"),
    )


def get_google_gemini_config() -> GoogleGeminiConfig:
    return GoogleGeminiConfig(api_key=os.environ.get("GOOGLE_API_KEY", ""))


def get_azure_content_safety_config() -> AzureContentSafetyConfig:
    return AzureContentSafetyConfig(
        endpoint=os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", ""),
        key=os.environ.get("AZURE_CONTENT_SAFETY_KEY", ""),
    )


def get_deepl_config() -> DeepLConfig:
    return DeepLConfig(auth_key=os.environ.get("DEEPL_AUTH_KEY", ""))


def get_firestore_config() -> FirestoreConfig:
    # Project ID will be inferred from GOOGLE_APPLICATION_CREDENTIALS
    return FirestoreConfig()
