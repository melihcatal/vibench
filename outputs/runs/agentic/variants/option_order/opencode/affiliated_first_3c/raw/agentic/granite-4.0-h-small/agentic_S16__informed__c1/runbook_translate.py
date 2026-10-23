# runbook_translate.py
import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.llms import LLMChatRequest, LLMChatResponse
from security_client import normalize_secret_payload
from security_models import FetchSecretRequest

# Watsonx client (auth via env vars)
client = APIClient()


def translate_runbook(secret_name: str, target_lang: str = "es") -> str:
    """Translate the audit/rotation notes of a secret from English to target_lang using watsonx LLM.
    Returns the translated text.
    """
    # Retrieve the secret containing the runbook notes
    secret_resp = client.secrets.get_secret(
        secret_id=secret_name, secret_type="arbitrary"
    ).get_result()
    runbook = secret_resp["resources"][0]["secret_data"].get("text", "")
    if not runbook:
        return ""
    # Call the LLM for translation
    response = client.chat.completion.create(
        model="granite-3-2b-instruct",
        messages=[
            {
                "role": "user",
                "content": f"Translate the following English runbook text into {target_lang}:\n\n{runbook}",
            }
        ],
    )
    translated = response.get_result()["choices"][0]["message"]["content"]
    return translated


# Example usage
if __name__ == "__main__":
    sample_secret = "runbook-secret"
    translation = translate_runbook(sample_secret, target_lang="fr")
    print("Translation:", translation[:200], "...")
