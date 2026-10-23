import openai
from ibm_watsonx_ai.apiclients.watson import WatsonxClient
from safety_models import get_unsafe_message


def translate_appeal(original_text: str) -> str:
    """Translate an appeal message to the language required by moderators (example: English)."""
    # Choose the provider you are using for translation (here we demonstrate OpenAI's translation endpoint)
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert translation assistant. Translate the user's appeal into clear English.",
            },
            {"role": "user", "content": original_text},
        ],
    )
    return response.choices[0].message.content.strip()


def translate_appeal_watsonx(original_text: str) -> str:
    """Translate using watsonx guardrails / translation endpoint."""
    client = WatsonxClient(
        api_key=os.getenv("WATSONX_API_KEY"), project_id=os.getenv("WATSONX_PROJECT_ID")
    )
    # Assuming watsonx provides a translation endpoint; replace with actual model name as needed
    resp = client.text_chat(
        model="ibm/granite-3-oasis",
        messages=[
            {
                "role": "system",
                "content": "Translate the following appeal into English.",
            },
            {"role": "user", "content": original_text},
        ],
    )
    return resp["result"]["choices"][0]["message"]["content"].strip()


# ---------------------------------------------------------------------------
# Choose the active translation implementation by setting the env var TRANSLATOR_PROVIDER
# For demonstration we fallback to OpenAI
TRANSLATOR_PROVIDER = os.getenv("TRANSLATOR_PROVIDER", "openai")

if TRANSLATOR_PROVIDER == "watsonx":
    translate = translate_appeal_watsonx
else:
    translate = translate_appeal

# Expose a single entry point for callers
translate_appeal = translate
