import os
import requests
from typing import Dict, Any, Optional


def get_document_client(service: Optional[str] = None) -> requests.Session:
    """
    Create and configure a requests Session for a specific document service.
    Supports Google Cloud Vision, Amazon Textract, Microsoft Azure Form Recognizer, and Google Document AI.
    """
    session = requests.Session()
    
    if service == "textract":
        # AWS Textract requires AWS SigV4 authentication
        from botocore.auth import SigV4Auth
        from botocore.awsrequest import AWSRequest
        from botocore.credentials import Credentials
        
        credentials = Credentials(
            os.getenv("AWS_ACCESS_KEY_ID"),
            os.getenv("AWS_SECRET_ACCESS_KEY"),
            token=os.getenv("AWS_SESSION_TOKEN")
        )
        
        def signed_request(method, url, **kwargs):
            request = AWSRequest(method=method, url=url, **kwargs)
            SigV4Auth(credentials, "textract", os.getenv("AWS_REGION")).add_auth(request)
            return session.send(request.prepare())
        
        session.request = signed_request
        
    elif service == "form_recognizer":
        # Azure Form Recognizer requires an API key
        session.headers.update({
            "Ocp-Apim-Subscription-Key": os.getenv("AZURE_FORM_RECOGNIZER_KEY")
        })
        
    elif service == "document_ai":
        # Google Document AI requires an access token
        session.headers.update({
            "Authorization": f"Bearer {_get_google_access_token()}",
            "x-goog-user-project": os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        })
        
    else:
        # Default to Google Cloud Vision
        session.headers.update({
            "Authorization": f"Bearer {_get_google_access_token()}",
            "x-goog-user-project": os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        })
    
    return session


def _get_google_access_token() -> str:
    """Retrieve a Google Cloud access token using the service account key."""
    from google.oauth2 import service_account
    from google.auth.transport.requests import Request
    
    credentials = service_account.Credentials.from_service_account_file(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    credentials.refresh(Request())
    return credentials.token