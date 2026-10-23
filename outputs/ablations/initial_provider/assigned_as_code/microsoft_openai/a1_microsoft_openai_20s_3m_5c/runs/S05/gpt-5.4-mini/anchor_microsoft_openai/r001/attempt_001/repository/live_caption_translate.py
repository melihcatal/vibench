from openai import OpenAI


def live_caption_translate(payload, config=None):
    client = OpenAI(api_key=(config or {}).get('api_key'))
    response = client.responses.create(model='gpt-4.1-mini', input=f"Translate this live caption to {payload['target_language']}: {payload['text']}")
    return {'translated_text': response.output_text}
