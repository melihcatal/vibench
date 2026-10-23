from amazon.ai.vision import StaticImage, VisualUnderstanding


def request_static_image(image_path):
    return StaticImage(image_path)


def request_visual_understanding(image_path):
    return VisualUnderstanding(image_path)


def normalize_static_image_response(response):
    return response.normalize()


def normalize_visual_understanding_response(response):
    return response.normalize()