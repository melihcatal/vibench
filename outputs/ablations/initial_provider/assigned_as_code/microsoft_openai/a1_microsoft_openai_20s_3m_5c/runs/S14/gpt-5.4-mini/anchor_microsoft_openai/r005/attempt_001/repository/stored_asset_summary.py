from openai import OpenAI

from storage_models import normalize_config, normalize_payload, object_response


def stored_asset_summary(payload, config=None):
    cfg = normalize_config(config)
    pl = normalize_payload(payload)
    client = OpenAI(api_key=cfg['openai_api_key'])
    completion = client.chat.completions.create(model=cfg.get('openai_model', 'gpt-4o-mini'), messages=[{'role': 'user', 'content': pl['text']}])
    return object_response(pl['object_name'], summary=completion.choices[0].message.content)
