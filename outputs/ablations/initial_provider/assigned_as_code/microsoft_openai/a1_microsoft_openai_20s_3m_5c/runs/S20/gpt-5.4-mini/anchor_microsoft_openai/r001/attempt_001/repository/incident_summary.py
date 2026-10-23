from observability_client import inference_clients, load_config


def incident_summary(payload, config=None):
    cfg = load_config(config)
    clients = inference_clients(cfg)
    rows = payload['rows']
    prompt = f"Summarize the incident from these Azure Monitor log rows for review: {rows}"
    response = clients['chat'].complete(messages=[{'role': 'user', 'content': prompt}], model=cfg.get('chat_model', 'gpt-4o-mini'))
    return {'summary': response.choices[0].message.content}
