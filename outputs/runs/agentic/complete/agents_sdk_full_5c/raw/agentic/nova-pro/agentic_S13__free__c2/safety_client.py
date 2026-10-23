import os
from perspectiveapi import PerspectiveAPI

def get_client():
    return PerspectiveAPI(api_key=os.getenv('PERSPECTIVE_API_KEY'))