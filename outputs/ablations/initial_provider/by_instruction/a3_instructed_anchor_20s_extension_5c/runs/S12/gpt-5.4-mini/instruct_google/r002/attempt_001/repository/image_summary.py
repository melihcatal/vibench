from vision_client import summarize_image


def image_summary(image_path: str) -> str:
    return summarize_image(image_path)
