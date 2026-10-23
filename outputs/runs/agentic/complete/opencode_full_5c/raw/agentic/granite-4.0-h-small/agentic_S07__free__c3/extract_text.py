# [SAME-SCENARIO] extract_text.py

import openai


def extract_text_from_image(image_path: str) -> str:
    """Extract plain text from a scanned document image using OpenAI's Vision model.

    Args:
        image_path: Path to the scanned image file.

    Returns:
        Extracted plain text.
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
                "description": "Extract text from this scanned document.",
            }
        ],
    )
    return response.choices[0].message.content
