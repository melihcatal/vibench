import os
from ibm_watsonx_ai import APIClient


def get_client():
    return APIClient(
        apikey=os.getenv("WATSONX_API_KEY"), project_id=os.getenv("WATSONX_PROJECT_ID")
    )
