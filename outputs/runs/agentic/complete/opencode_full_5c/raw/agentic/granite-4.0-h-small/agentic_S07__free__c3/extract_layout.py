# [SAME-SCENARIO] extract_layout.py

import openai


def extract_layout_from_image(image_path: str) -> str:
    """Extract layout elements (blocks, lines, tables, etc.) from a document image using OpenAI's Vision model.

    Args:
        image_path: Path to the scanned image file.

    Returns:
        JSON string representing detected layout elements.
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
                "description": "Extract layout elements (blocks, lines, tables, etc.) from this document.",
            }
        ],
    )
    return response.choices[0].message.content
