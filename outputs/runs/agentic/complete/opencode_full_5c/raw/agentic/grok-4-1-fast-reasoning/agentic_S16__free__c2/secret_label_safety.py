import os
from security_client import get_secrets_client
from openai import OpenAI


def check_secret_labels_notes_safety(secret_name: str) -> dict:
    client = get_secrets_client()
    desc_resp = client.describe_secret(SecretId=secret_name)
    notes = desc_resp.get("Description", "")
    tags = desc_resp.get("Tags", [])
    label_text = (
        notes
        + " "
        + " ".join([f"{tag.get('Key', '')}:{tag.get('Value', '')}" for tag in tags])
    )
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    mod_resp = openai_client.moderations.create(
        input=label_text, model="text-moderation-latest"
    )
    result = mod_resp.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores),
    }
