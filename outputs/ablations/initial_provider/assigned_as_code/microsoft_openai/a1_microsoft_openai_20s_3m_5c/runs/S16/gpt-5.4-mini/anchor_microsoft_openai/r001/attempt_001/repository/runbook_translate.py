from openai import OpenAI

from security_client import load_config


def runbook_translate(payload, config=None):
    config = load_config(config)
    client = OpenAI(api_key=config['openai_api_key'])
    completion = client.responses.create(model='gpt-4.1-mini', input=payload['notes'], instructions='Translate the secret-rotation runbook notes to the requested language.')
    return {'translation': completion.output_text}
