import os
import requests

# Azure Content Moderator endpoint and key
# AZURE_CONTENT_MODERATOR_ENDPOINT
# AZURE_CONTENT_MODERATOR_KEY

def moderate_free_text_claims(text_claim, language="eng"):
    endpoint = os.environ.get("AZURE_CONTENT_MODERATOR_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_MODERATOR_KEY")

    if not endpoint or not key:
        return {"error": "Azure Content Moderator endpoint or key not configured."}

    text_moderation_url = f"{endpoint}/contentmoderator/moderate/v2.0/ProcessText/Screen?language={language}"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "text/plain"
    }

    try:
        response = requests.post(text_moderation_url, headers=headers, data=text_claim.encode('utf-8'))
        response.raise_for_status()
        result = response.json()
        return {"moderation_result": result}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
