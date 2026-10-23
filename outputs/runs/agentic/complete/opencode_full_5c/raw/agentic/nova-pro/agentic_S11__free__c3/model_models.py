import json


def normalize_request(request):
    return json.dumps(request)


def parse_response(response):
    return json.loads(response)
