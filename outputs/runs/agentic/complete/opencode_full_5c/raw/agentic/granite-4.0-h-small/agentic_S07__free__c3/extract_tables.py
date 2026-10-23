# [SAME-SCENARIO] extract_tables.py

import openai


def extract_tables_from_image(image_path: str) -> str:
    """Extract tables (cells and row structure) from a scanned document image.

    Args:
        image_path: Path to the scanned image file.

    Returns:
        JSON string representing the table structure.
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
                "description": "Extract table cells and row structure from this document.",
            }
        ],
    )
    return response.choices[0].message.content
