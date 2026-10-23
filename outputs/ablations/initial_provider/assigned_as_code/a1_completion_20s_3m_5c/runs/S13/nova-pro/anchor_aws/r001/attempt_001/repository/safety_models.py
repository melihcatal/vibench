def format_batch_request(payloads):
    return {'TextSegments': [{'Text': p['text']} for p in payloads], 'LanguageCode': 'en'}


def parse_batch_response(response):
    return [{'toxicity': r['Toxicity']} for r in response['ResultList']]


def format_redact_request(payload):
    return {'Text': payload['text'], 'LanguageCode': 'en'}


def parse_redact_response(response):
    return {'redacted_text': response['RedactedText']}


def format_threshold_request(payload):
    return {'TextSegments': [{'Text': payload['text']}], 'LanguageCode': 'en'}


def parse_threshold_response(response):
    return {'toxicity': response['ResultList'][0]['Toxicity']}