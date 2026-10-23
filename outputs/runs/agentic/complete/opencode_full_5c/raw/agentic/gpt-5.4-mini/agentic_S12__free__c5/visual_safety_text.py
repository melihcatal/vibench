from vision_client import create_client, load_config
from vision_models import normalize_response


def visual_safety_text(text: str):
    config = load_config()
    client = create_client(config)
    response = client.responses.create(
        model=config.model,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"Check the following visual labels or description text for unsafe, hateful, sexual, violent, or policy-sensitive content. Return a short classification and rationale: {text}",
                    }
                ],
            }
        ],
    )
    return normalize_response(response)
