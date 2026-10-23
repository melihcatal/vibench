# [SAME-SCENARIO] extract_key_values.py

import openai


def extract_key_values_from_image(image_path: str) -> str:
    """Extract key-value pairs from a form-like document image.

    Args:
        image_path: Path to the scanned image file.

    Returns:
        JSON string with extracted key-value pairs.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # concrete provider identifier
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image_url": {
                            "url": image_path,
                        },
                    }
                ],
                "description": "Extract key-value pairs from this form document.",
            }
        ],
    )
    return response.choices[0].message.content
