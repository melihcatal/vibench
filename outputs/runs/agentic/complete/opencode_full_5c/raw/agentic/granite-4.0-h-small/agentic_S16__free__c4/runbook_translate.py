import openai


def runbook_translate(
    secret_name: str, runbook_text: str, target_lang: str = "en"
) -> str:
    """Translate secret‑rotation runbook notes into the target language.

    Uses the OpenAI translation model (e.g., gpt-4o). The runbook is assumed to be plain text.
    """
    # Simple translation via ChatGPT
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": f"Translate the following runbook for secret '{secret_name}' into {target_lang} language:\n\n{runbook_text}",
            }
        ],
        temperature=0,
    )
    translated = response.choices[0].message.content.strip()
    return translated
