import dashscope

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")


def detect_image_text(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    response = dashscope.Vision.detect_text(image_data)
    return response.outputs["text"]
