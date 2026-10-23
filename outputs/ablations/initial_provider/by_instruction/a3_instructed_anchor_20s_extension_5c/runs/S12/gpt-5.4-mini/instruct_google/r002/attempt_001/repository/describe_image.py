from vision_client import summarize_image


def describe_image(image_path: str) -> str:
    return summarize_image(image_path)
