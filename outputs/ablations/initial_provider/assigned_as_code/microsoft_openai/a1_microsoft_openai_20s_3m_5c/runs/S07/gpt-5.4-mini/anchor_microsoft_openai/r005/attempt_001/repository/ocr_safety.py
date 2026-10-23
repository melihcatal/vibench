import requests


def ocr_safety(payload, config=None):
    config = config or {}
    response = requests.post(f"{config['safety_endpoint']}/contentsafety/text:analyze?api-version=2024-09-01", headers={'Ocp-Apim-Subscription-Key': config['safety_key'], 'Content-Type': 'application/json'}, json={'text': payload.get('text', '')})
    response.raise_for_status()
    data = response.json()
    return {'unsafe': any(item.get('severity', 0) > 0 for item in data.get('categoriesAnalysis', [])), 'analysis': data}
