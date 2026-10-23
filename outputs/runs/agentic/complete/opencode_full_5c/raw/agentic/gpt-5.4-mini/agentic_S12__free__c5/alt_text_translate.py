from vision_client import create_client, load_config
from vision_models import normalize_response


def alt_text_translate(text: str, target_language: str):
    config = load_config()
    client = create_client(config)
    response = client.responses.create(
        model=config.translation_model,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"Translate this image description into {target_language}: {text}",
                    }
                ],
            }
        ],
    )
    return normalize_response(response)
