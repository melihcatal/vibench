import perspective

def check_safety(text):
    client = perspective.Client()
    attributes = ['TOXICITY', 'IDENTITY_ATTACK', 'INSULT', 'PROFANITY', 'THREAT']
    response = client.analyze(text, attributes)
    return response