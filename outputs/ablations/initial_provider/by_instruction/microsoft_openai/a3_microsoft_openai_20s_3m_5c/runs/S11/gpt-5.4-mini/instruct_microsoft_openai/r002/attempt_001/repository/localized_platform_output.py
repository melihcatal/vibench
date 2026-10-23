from model_client import create_platform_client, load_platform_config


def localized_platform_output(text: str, locale: str) -> str:
    config = load_platform_config()
    client = create_platform_client(config)
    result = client.responses.create(model=config.deployment, input=f"Translate to {locale}: {text}")
    return result.output_text
