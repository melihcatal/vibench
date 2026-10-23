import openai
import os


def check_secret_labels_safety(labels_notes):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    moderation = client.moderations.create(
        input=labels_notes, model="text-moderation-latest"
    )
    return moderation.results[0]
