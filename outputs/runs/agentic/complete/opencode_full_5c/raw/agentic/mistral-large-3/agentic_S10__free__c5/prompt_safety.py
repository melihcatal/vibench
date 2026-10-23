from typing import Optional, Dict, Any
import os
from google.cloud import language_v1
from google.oauth2 import service_account


def check_prompt_safety(
    text: str,
    language: str = "en",
    api_key: Optional[str] = None,
    credentials_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Check prompts and generated text for unsafe content using Google Cloud Natural Language API.
    """
    if credentials_path:
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
    else:
        credentials = service_account.Credentials.from_service_account_info(
            {
                "type": os.getenv("GOOGLE_TYPE"),
                "project_id": os.getenv("GOOGLE_PROJECT_ID"),
                "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
                "private_key": os.getenv("GOOGLE_PRIVATE_KEY").replace("\\n", "\n"),
                "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "auth_uri": os.getenv("GOOGLE_AUTH_URI"),
                "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
                "auth_provider_x509_cert_url": os.getenv(
                    "GOOGLE_AUTH_PROVIDER_CERT_URL"
                ),
                "client_x509_cert_url": os.getenv("GOOGLE_CLIENT_CERT_URL"),
            }
        )

    client = language_v1.LanguageServiceClient(credentials=credentials)
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT, language=language
    )

    response = client.analyze_sentiment(request={"document": document})

    response = client.moderate_text(request={"document": document})

    return {
        "sentiment": {
            "score": response.document_sentiment.score,
            "magnitude": response.document_sentiment.magnitude,
        },
        "moderation": {
            "blocked": any(
                category.confidence > 0.8 for category in response.moderation_categories
            ),
            "categories": [
                {"name": category.name, "confidence": category.confidence}
                for category in response.moderation_categories
            ],
        },
    }
