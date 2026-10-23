import dashscope

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")


def image_summary(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    response = dashscope.Vision.summarize_image(image=image_data)
    return response.body["summary"]
