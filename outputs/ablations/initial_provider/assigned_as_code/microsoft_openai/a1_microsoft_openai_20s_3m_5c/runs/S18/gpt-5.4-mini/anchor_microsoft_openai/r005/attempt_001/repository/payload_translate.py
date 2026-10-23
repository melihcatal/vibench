import requests
from messaging_client import load_messaging_config


def translate_payload_text(text, target_language='es', config=None):
    cfg = load_messaging_config(config)
    response = requests.post(
        f"{cfg['translator_resource']}/translate?api-version=3.0&to={target_language}",
        headers={'Ocp-Apim-Subscription-Key': cfg['translator_key'], 'Content-Type': 'application/json'},
        json=[{'text': text}],
        timeout=10,
    )
    response.raise_for_status()
    return {'translated_text': response.json()[0]['translations'][0]['text']}
