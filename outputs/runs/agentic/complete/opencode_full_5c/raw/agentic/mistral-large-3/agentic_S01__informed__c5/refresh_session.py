import os
import requests
from identity_client import IBMAppIDClient
from identity_models import RefreshRequest, RefreshResponse, normalize_refresh_response


def refresh_session(refresh_token: str) -> RefreshResponse:
    client = IBMAppIDClient()
    return client.refresh_session(RefreshRequest(refresh_token=refresh_token))
