from translation_client import load_translation_config


def translation_memory_embedding(payload, config=None):
    cfg = load_translation_config(config)
    return {'model': 'text-embedding-3-small', 'provider': 'openai', 'api_key_present': bool(cfg['api_key']), 'segments': payload['segments']}
