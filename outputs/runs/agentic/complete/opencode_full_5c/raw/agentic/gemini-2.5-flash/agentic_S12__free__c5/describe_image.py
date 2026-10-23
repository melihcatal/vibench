import os
from vision_client import get_gemini_pro_vision_model
from vision_models import load_image_from_file
import PIL.Image


def describe_image(image_path: str, prompt: str = "Describe this image.") -> str:
    model = get_gemini_pro_vision_model()
    image_bytes = load_image_from_file(image_path)
    image = PIL.Image.open(image_path)  # PIL for image handling with Gemini

    response = model.generate_content([prompt, image])
    return response.text


if __name__ == "__main__":
    # Example usage: Replace with your image path
    # Ensure GOOGLE_API_KEY environment variable is set.
    dummy_image_path = "test_image.jpg"
    if not os.path.exists(dummy_image_path):
        # Create a tiny black image if it doesn't exist
        try:
            from PIL import Image

            img = Image.new("RGB", (1, 1), color="black")
            img.save(dummy_image_path)
        except ImportError:
            print(
                "Pillow not installed. Cannot create dummy image. Please install with `pip install Pillow`"
            )
            with open(dummy_image_path, "w") as f:
                f.write("dummy content for text-based fallback")

    description = describe_image(dummy_image_path)
    print(f"Image description: {description}")
