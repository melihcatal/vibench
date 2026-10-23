import requests

from storage_models import normalize_config, normalize_payload, object_response


def stored_text_translate(payload, config=None):
    cfg = normalize_config(config)
    pl = normalize_payload(payload)
    response = requests.post(
        f"{cfg['translator_endpoint'].rstrip('/')}/translate?api-version=3.0&to={pl.get('target_language', 'en')}",
        headers={'Ocp-Apim-Subscription-Key': cfg['translator_key'], 'Ocp-Apim-Subscription-Region': cfg.get('translator_region', 'global'), 'Content-Type': 'application/json'},
        json=[{'text': pl['text']}],
        timeout=30,
    )
    translated = response.json()[0]['translations'][0]['text']
    return object_response(pl['object_name'], translated_text=translated)
