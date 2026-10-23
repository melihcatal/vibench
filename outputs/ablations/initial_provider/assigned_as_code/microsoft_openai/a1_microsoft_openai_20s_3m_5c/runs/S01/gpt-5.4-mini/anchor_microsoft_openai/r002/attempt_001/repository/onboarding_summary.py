import os

from openai import OpenAI

from identity_models import require_fields


def onboarding_summary(payload, config=None):
    payload = require_fields(payload, ['state'])
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    result = client.responses.create(model='gpt-5.4-mini', input='Summarize this onboarding state for support: ' + str(payload['state']))
    return {'summary': result.output_text}
