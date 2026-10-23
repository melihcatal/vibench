import openai

from vision_client import load_vision_config


def visual_safety_text(payload, config=None):
    cfg = load_vision_config(config)
    client = openai.OpenAI(api_key=cfg.get('api_key'))
    labels = payload.get('labels', [])
    prompt = 'Assess whether these visual labels are unsafe: ' + ', '.join(labels)
    result = client.chat.completions.create(model='gpt-5.4-mini', messages=[{'role': 'user', 'content': prompt}])
    return {'assessment': result.choices[0].message.content}
