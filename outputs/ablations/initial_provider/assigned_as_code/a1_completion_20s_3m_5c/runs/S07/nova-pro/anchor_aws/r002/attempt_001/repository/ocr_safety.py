import perspectiveapi


def check_safety(text):
    client = perspectiveapi.Client()
    analysis = client.analyze(text, attributes=['TOXICITY', 'IDENTITY_ATTACK', 'INSULT', 'PROFANITY', 'THREAT'])
    return analysis