def normalize_payload(payload):
    return {'Text': payload['text']}


def parse_response(response, redact=False):
    toxicity_scores = response['ResultList'][0]['ToxicityScores']
    if redact:
        redacted_text = response['ResultList'][0]['RedactedText']
        return redacted_text
    return toxicity_scores