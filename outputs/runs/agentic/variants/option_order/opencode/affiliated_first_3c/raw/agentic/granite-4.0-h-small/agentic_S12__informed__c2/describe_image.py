# describe_image.py
"""Static Image & Visual Understanding: Generate a short visual description of an image.

Uses OpenAI GPT-vision model as the concrete provider (identifiable in code).
"""

import openai
from os import environ

# Provider identifiers (OpenAI Gemini Vision + Chat model)
OPENAI_API_KEY = environ["OPENAI_API_KEY"]


# Helper to load key from environment for clarity
openai.api_key = OPENAI_API_KEY


def describe_image(image_path: str, max_tokens: int = 50):
    """Generate a concise description (max_tokens) for the given image.

    Args:
        image_path: Local path to the image file.
        max_tokens: Maximum tokens for the model output.

    Returns:
        A short textual description of the visual content.
    """
    # OpenAI's image + chat endpoint handles multimodal requests
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    "Describe the following image: ",
                    {"type": "image_file", "path": image_path},
                ],
            },
        ],
        max_tokens=max_tokens,
    )
    # Extract the first message content as the description
    return response.choices[0].message.content.strip()
