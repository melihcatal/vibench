import os
from openai import OpenAI

OPENAI_SUMMARY_MODEL = 'gpt-4.1-mini'


def onboarding_summary(state):
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    response = client.responses.create(model=OPENAI_SUMMARY_MODEL, input=f'Summarize onboarding state for support: {state}')
    return response.output_text
