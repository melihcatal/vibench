import os
from perspectiveapi import PerspectiveAPI

def moderate_text(text):
    client = PerspectiveAPI()
    response = client.analyze(text, ['TOXICITY'])
    return response['attributeScores']['TOXICITY']['summaryScore']['value'] < 0.5