import vertexai
from vertexai.generative_models import GenerativeModel, Part
from vision_models import ImageDescription


def describe_image(image_path: str) -> ImageDescription:
    model = GenerativeModel("gemini-1.0-pro-vision")

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    image_part = Part.from_data(data=image_bytes, mime_type="image/jpeg")

    prompt = "Describe this image in one sentence."

    response = model.generate_content([image_part, prompt])

    return ImageDescription(text=response.text)
