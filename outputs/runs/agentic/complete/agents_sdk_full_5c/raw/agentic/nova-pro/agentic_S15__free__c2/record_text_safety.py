import os
import perspective_api

client = perspective_api.Client(os.getenv('PERSPECTIVE_API_KEY'))

def check_text_safety(text):
    analysis = client.analyze(text, requested_attributes=['TOXICITY'])
    return analysis['attributeScores']['TOXICITY']['summaryScore']['value'] < 0.5