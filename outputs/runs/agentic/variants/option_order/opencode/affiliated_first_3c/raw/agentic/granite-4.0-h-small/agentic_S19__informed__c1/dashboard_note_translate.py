import os
from observable_client import get_provider_client
from observable_models import QueryMetricWindowRequest

PROVIDER = os.getenv("METRICS_PROVIDER", "datadog")


def translate_dashboard_note(note_text: str, target_locale: str = "es") -> str:
    """Translate a metric/dashboard note to another locale using the configured provider's LLM.

    The function demonstrates a later‑step integration that could be expanded to integrate
    with a dedicated translation service (Amazon Translate, Google Translate, etc.).
    Here we use a generic LLM client (watsonx, Gemini, etc.) as a placeholder.

    Returns the translated text.
    """
    client = get_provider_client(PROVIDER)
    # Example using watsonx.ai text generation as a translation service
    if PROVIDER == "watsonx":
        # watsonx.ai text chat endpoint (simplified)
        response = client.chat(
            system="You are a translation assistant.",
            user=f"Translate the following note to {target_locale}: {note_text}",
        )
        return response.choices[0].message.content.strip()
    elif PROVIDER == "gemini":
        # Gemini API translation (pseudo‑code)
        from google.generativeai import GenerativeModel

        model = GenerativeModel("gemini-1.5-flash")
        return model.generate_content(f"Translate to {target_locale}: {note_text}").text
    elif PROVIDER == "anthropic":
        # Anthropic Messages API
        from anthropic import Anthropic, HumanMessage

        client = Anthropic()
        messages = [HumanMessage(content=f"Translate to {target_locale}: {note_text}")]
        response = client.messages.create(
            model="claude-3-opus-20240229", messages=messages
        )
        return response.content[0].text
    elif PROVIDER == "openai":
        # OpenAI Chat Completion
        from openai import OpenAI

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a translation assistant."},
                {
                    "role": "user",
                    "content": f"Translate the following note to {target_locale}: {note_text}",
                },
            ],
            max_tokens=256,
        )
        return resp.choices[0].message.content.strip()
    else:
        raise ValueError(f"Translation not supported for provider {PROVIDER}")


if __name__ == "__main__":
    sample_note = "High CPU usage detected on production servers."
    translated = translate_dashboard_note(sample_note, target_locale="fr")
    print("French translation:", translated)
