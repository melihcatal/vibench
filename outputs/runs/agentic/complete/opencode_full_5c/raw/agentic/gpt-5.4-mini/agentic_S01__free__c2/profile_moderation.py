import os
from openai import OpenAI

OPENAI_MODERATION_MODEL = 'omni-moderation-latest'


def profile_moderation(text):
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    return client.moderations.create(model=OPENAI_MODERATION_MODEL, input=text).results[0]
