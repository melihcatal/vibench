import perspective

def check_text_safety(text):
    client = perspective.Client('default')
    results = client.analyze([text], ['TOXICITY'])
    return results[0]['TOXICITY']