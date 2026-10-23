import re
from security_models import SecretResponse
from secret_clients import SecretsManagerClient


def secret_label_safety(secret_name: str) -> bool:
    """Checks secret labels/notes for unsafe text using Perspective API.
    Args:
        secret_name (str): Name of the secret to evaluate.
    Returns:
        bool: True if safe, False if unsafe language detected.
    """
    client = SecretsManagerClient()
    response = client.get_secret_value(SecretId=secret_name)
    text = response.get("SecretString", "")
    payload = {"comment": text, "languages": ["en"]}
    resp = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": os.getenv("PERSPECTIVE_API_KEY")},
        json=payload,
    )
    attr = resp.json()["attributeScores"].get("TOXICITY", {}).get("summaryScore", {})
    return attr["value"] < 0.5
