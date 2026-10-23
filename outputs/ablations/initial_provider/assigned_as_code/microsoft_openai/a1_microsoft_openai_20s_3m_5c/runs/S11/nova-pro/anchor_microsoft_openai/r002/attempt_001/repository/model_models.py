from invoke_platform_model import invoke_platform_model


def normalize_request(payload):
    return {'text': payload['text']}


def normalize_response(response):
    return {'text': response['text']}