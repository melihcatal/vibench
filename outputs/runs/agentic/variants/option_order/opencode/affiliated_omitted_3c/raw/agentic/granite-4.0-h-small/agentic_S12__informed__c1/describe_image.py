# describe_image.py - Generate a short visual description for an image using Qwen-VL via DashScope

from vision_client import VisionClient
from vision_models import normalize_description_response

# DashScope credentials (use env vars or config in production)
DASHSCOPE_API_KEY = "YOUR_DASHSCOPE_API_KEY"
REGION = "cn-hangzhou"

# Create a singleton client
VISION_CLIENT = VisionClient(
    region=REGION,
    api_key=DASHSCOPE_API_KEY,
)


def describe_image(image_path: str):
    """Generate a concise image description using Qwen-VL.

    Returns a single string containing the description.
    """
    resp = VISION_CLIENT.generate_caption(image_path=image_path)
    # normalize to our expected structure (single description string in a list)
    return normalize_description_response(resp)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: describe_image.py <image_path>")
        sys.exit(1)
    description = describe_image(sys.argv[1])
    print(description["description"])
