from observability_client import inference_clients, load_config


def log_text_safety(payload, config=None):
    cfg = load_config(config)
    clients = inference_clients(cfg)
    text = payload['text']
    prompt = f"Classify whether this support-visible log text is unsafe, toxic, secret-leaking, or sensitive: {text}. Return JSON with safe and reasons."
    response = clients['chat'].complete(messages=[{'role': 'user', 'content': prompt}], model=cfg.get('chat_model', 'gpt-4o-mini'))
    return {'analysis': response.choices[0].message.content}
