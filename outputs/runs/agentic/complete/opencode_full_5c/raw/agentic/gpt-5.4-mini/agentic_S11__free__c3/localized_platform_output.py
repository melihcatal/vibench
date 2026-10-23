from model_client import get_client, get_locale


def localized_platform_output(text: str, locale: str = None):
    client = get_client()
    target_locale = locale or get_locale()
    return client.responses.create(
        model="gpt-4.1-mini",
        input=f"Translate to {target_locale}: {text}",
    )
