import os
from dashscope import Vision


def score_image_safety(image_path):
    api_key = os.getenv("DASHSCOPE_API_KEY")
    client = Vision(api_key=api_key)
    response = client.score_safety(image_path)
    return response.safety_score
