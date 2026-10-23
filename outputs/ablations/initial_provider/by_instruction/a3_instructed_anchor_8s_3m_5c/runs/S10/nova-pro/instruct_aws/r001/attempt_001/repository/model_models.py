import json

def normalize_response(response):
    return json.loads(response['body'].read())

def extract_output_text(result):
    return result['results'][0]['outputText']