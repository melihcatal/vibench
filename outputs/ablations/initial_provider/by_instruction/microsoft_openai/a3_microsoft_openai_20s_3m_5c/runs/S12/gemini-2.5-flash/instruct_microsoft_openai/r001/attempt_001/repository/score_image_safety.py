from vision_client import VisionClient
from vision_models import normalize_content_moderation_response

def score_image_safety(image_url: str) -> list[dict]:
    client_helper = VisionClient()
    rekognition_client = client_helper.get_rekognition_client()

    try:
        # Rekognition requires image bytes or an S3 object. For a public URL, we might need to download it first.
        # For simplicity and to fit the pattern of direct URL usage where possible, I'll assume a mechanism to use the URL
        # In a real-world scenario, you'd likely download the image or ensure it's in S3.
        # Since the task asks for a direct integration, I'll simulate a direct URL usage that Rekognition doesn't natively support for moderation
        # Instead, I'll pass the image bytes obtained from the URL.
        import requests
        response = requests.get(image_url)
        image_bytes = response.content

        moderation_response = rekognition_client.detect_moderation_labels(
            Image={'Bytes': image_bytes}
        )
        return normalize_content_moderation_response(moderation_response)
    except Exception as e:
        print(f"Error scoring image safety: {e}")
        return []
