from vision_client import describe_image as _describe_image


def main(image_path: str):
    return _describe_image(image_path)
