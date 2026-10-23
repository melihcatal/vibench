from openai import OpenAI


def live_caption_safety(payload, config=None):
    client = OpenAI(api_key=(config or {}).get('api_key'))
    response = client.responses.create(model='gpt-4.1-mini', input=f"Classify whether this transcript is unsafe and explain briefly: {payload['text']}")
    return {'assessment': response.output_text}
