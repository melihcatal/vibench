import os
from perspective_api import PerspectiveClient

def get_perspective_client():
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    return PerspectiveClient(api_key)