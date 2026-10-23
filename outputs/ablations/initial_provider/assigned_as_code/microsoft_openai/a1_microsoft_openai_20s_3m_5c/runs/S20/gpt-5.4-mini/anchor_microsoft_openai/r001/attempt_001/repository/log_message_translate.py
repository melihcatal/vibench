from observability_client import inference_clients, load_config


def log_message_translate(payload, config=None):
    cfg = load_config(config)
    clients = inference_clients(cfg)
    text = payload['text']
    locale = payload.get('locale', 'es')
    prompt = f"Translate this support-visible log message into {locale}, keeping technical identifiers intact: {text}"
    response = clients['chat'].complete(messages=[{'role': 'user', 'content': prompt}], model=cfg.get('chat_model', 'gpt-4o-mini'))
    return {'translation': response.choices[0].message.content, 'locale': locale}
