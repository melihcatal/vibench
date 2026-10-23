import os
import requests

CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
API_IDENTIFIER = os.getenv("AUTH0_API_IDENTIFIER")


def get_auth0_client():
    return requests.Session()
