from typing import Optional, Dict, Any
import os
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account


def translate_result(
    text: str,
    target_language: str = "es",
    source_language: Optional[str] = None,
    api_key: Optional[str] = None,
    credentials_path: Optional[str] = None,
) -> str:
    """
    Translate generated model output using Google Cloud Translation API.
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

    client = translate.Client(credentials=credentials)
    result = client.translate(
        text, target_language=target_language, source_language=source_language
    )

    return result["translatedText"]
