def normalize_response(response):
    return response['body'].read().decode('utf-8')

def parse_response(response):
    return json.loads(normalize_response(response))