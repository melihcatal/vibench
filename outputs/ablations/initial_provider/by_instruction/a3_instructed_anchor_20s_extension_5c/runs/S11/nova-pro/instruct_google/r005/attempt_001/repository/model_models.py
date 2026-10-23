from.model_client import get_model_client

def normalize_request(instances):
    return {"instances": instances}

def parse_response(response):
    return response.predictions