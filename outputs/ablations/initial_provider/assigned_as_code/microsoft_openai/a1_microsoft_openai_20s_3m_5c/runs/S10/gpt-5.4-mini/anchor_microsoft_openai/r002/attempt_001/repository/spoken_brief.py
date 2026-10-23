from openai import OpenAI
from model_client import get_config, get_model


def spoken_brief(payload, config=None):
    resolved = get_config(config)
    text = payload.get('text') or ''
    prompt = 'Convert the following model output into a concise spoken brief suitable for audio playback.\n\n' + text
    with OpenAI(api_key=resolved['api_key']) as client:
        response = client.chat.completions.create(model=get_model(config), messages=[{'role': 'user', 'content': prompt}])
    return {'text': response.choices[0].message.content or ''}
