from .model_client import get_client, get_model_id


def create_request(prompt):
    return {"model": get_model_id(), "prompt": prompt}


def normalize_response(response):
    return response.output.choices[0].message.content
