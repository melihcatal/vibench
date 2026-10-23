# [LATER-STEP] live_caption_safety.py

# Identify provider: OpenAI Moderation
import openai


def check_safety(text: str) -> bool:
    response = openai.Moderation.create(input=text)
    flagged = response["results"][0]["flagged"]
    return not flagged  # returns True if safe
