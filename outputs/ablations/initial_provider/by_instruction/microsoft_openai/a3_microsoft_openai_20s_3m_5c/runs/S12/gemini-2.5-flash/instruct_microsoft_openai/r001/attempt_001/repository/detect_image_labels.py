from vision_client import VisionClient
from vision_models import normalize_labels_response

def detect_image_labels(image_url: str) -> list[str]:
    client_helper = VisionClient()
    openai_client = client_helper.get_openai_client()

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o", # Concrete model identifier for OpenAI
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What are the objects or labels in this image? Provide a concise comma-separated list."},
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url, "detail": "low"},
                        },
                    ],
                }
            ],
            max_tokens=300,
        )
        return normalize_labels_response(response.model_dump())
    except Exception as e:
        print(f"Error detecting image labels: {e}")
        return []
