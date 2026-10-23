from observability_client import ObservabilityClient


def dashboard_note_translate(text: str, target_locale: str):
    client = ObservabilityClient(endpoint="https://api.openai.com/v1")
    return client.post("/responses", {"model": "gpt-5.4-mini", "input": f"Translate to {target_locale}: {text}"})
