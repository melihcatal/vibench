DO NOT REMOVE THIS LINE - CONTENT BELOW IS EDITABLE BY THE ASSISTANT

Purpose: Local configuration utilities for Email/Password Account Lifecycle

---

# Identity Client Helpers

```python
import os
import json
from typing import Any, Dict

# Auth0 Management API
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')

# Amazon Cognito credentials
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
REGION_NAME = os.getenv('AWS_REGION', 'us-east-1')
COGNITO_USER_POOL_ID = os.getenv('COGNITO_USER_POOL_ID')
COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')

# Helper to obtain Auth0 Management API client
def get_auth0_client() -> Any:
    """Return an Auth0 Management API client using env vars."""
    from auth0.v3.management import Client
    from auth0.v3.authentication import GetToken
    token = GetToken(AUTH0_DOMAIN).get_access_token(AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET)
    return Client(token, AUTH0_DOMAIN)

# Helper to obtain boto3 Cognito Identity Provider client
def get_cognito_client() -> Any:
    """Return a boto3 Cognito Identity Provider client."""
    import boto3
    return boto3.client(
        'cognito-idp',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=REGION_NAME
    )

# Minimal request/response wrapper for email/password flow
RequestPayload = Dict[str, Any]
ResponsePayload = Dict[str, Any]

def serialize_payload(data: RequestPayload) -> str:
    """Convert dictionary to JSON string ensuring UTF-8 encoding."""
    return json.dumps(data, ensure_ascii=False)

def deserialize_response(raw: str) -> ResponsePayload:
    """Parse JSON string into Python dict."""
    return json.loads(raw)
```
