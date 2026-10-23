import os
import mindee


def get_client():
    return mindee.Client(api_key=os.getenv("MINDEE_API_KEY"))


def normalize_response(response):
    # Normalization logic here
    pass
