from openai import AzureOpenAI


def platform_brief_audio(payload, config=None):
    config = config or {}
    prompt = f"Create a short spoken briefing from this text: {payload['text']}"
    with AzureOpenAI(azure_endpoint=config['endpoint'], api_key=config['api_key'], api_version=config.get('api_version', '2024-10-21')) as client:
        response = client.audio.speech.create(model=config.get('speech_model', 'gpt-4o-mini-tts'), voice=config.get('voice', 'alloy'), input=prompt)
    return {'audio': response, 'format': 'mp3'}
