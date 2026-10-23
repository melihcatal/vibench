from openai import OpenAI
from vision_client import get_openai_api_key

def generate_image_description(image_url: str, prompt: str = "Describe this image in one sentence.") -> str:
    """
    Generates a short visual description for an image using OpenAI's GPT-4 with Vision.
    """
    api_key = get_openai_api_key()
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
        
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )

    if response.choices:
        return response.choices[0].message.content
    else:
        return "No description could be generated."
