import perspective

def check_safety(text):
    client = perspective.Client()
    response = client.analyze(text, ['TOXICITY'])
    return response['TOXICITY']['score'] < 0.5