import dashscope

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")


def score_image_safety(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    response = dashscope.Vision.score_safety(image=image_data)
    return response.body["safety_score"]
