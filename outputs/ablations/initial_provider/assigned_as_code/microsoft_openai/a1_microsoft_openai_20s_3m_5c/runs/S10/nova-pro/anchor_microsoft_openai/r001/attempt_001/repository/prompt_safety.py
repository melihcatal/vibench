from.model_client import get_client

def check_safety(payload, config=None):
    client = get_client(config)
    response = client.moderations.create(input=payload['text'])
    return {'safe': not response.results[0].flagged}