from vision_client import VisionClient
from vision_models import normalize_description_response

def describe_image(image_url: str) -> str:
    client_helper = VisionClient()
    openai_client = client_helper.get_openai_client()

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o", # Concrete model identifier for OpenAI
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Generate a short, concise visual description of this image."},
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url, "detail": "low"},
                        },
                    ],
                }
            ],
            max_tokens=100,
        )
        return normalize_description_response(response.model_dump())
    except Exception as e:
        print(f"Error describing image: {e}")
        return ""
