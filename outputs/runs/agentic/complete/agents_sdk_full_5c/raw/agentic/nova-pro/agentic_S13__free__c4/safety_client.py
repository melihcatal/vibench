import os
from google.cloud import perspective

def get_perspective_client():
    return perspective.Client(api_key=os.getenv('PERSPECTIVE_API_KEY'))