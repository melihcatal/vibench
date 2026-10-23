from .model_client import get_model


def normalize_request(prompt):
    return {"prompt": prompt}


def normalize_response(response):
    return response.outputs[0].text
