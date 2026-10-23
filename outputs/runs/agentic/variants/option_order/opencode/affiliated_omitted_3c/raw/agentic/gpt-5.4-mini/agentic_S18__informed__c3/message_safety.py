import requests


def check_message_safety(text):
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    response = requests.post(url, params={"key": api_key}, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    return {"safe": data.get("attributeScores", {}).get("TOXICITY", {}).get("summaryScore", {}).get("value", 0) < 0.5, "raw": data}
