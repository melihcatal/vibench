import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def safety_threshold(text, threshold=0.5):
    response = openai.Moderation.create(input=text)
    score = response.results[0].categories['sexual']
    return score < threshold