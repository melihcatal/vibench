from vision_client import create_client, load_config
from vision_models import normalize_response


def image_summary(
    labels_text: str = "", description_text: str = "", ocr_text: str = ""
):
    config = load_config()
    client = create_client(config)
    prompt = (
        "Summarize the visual analysis results into a compact structured paragraph."
    )
    payload = f"Labels: {labels_text}\nDescription: {description_text}\nOCR: {ocr_text}"
    response = client.responses.create(
        model=config.model,
        input=[
            {
                "role": "user",
                "content": [{"type": "input_text", "text": prompt + "\n" + payload}],
            }
        ],
    )
    return normalize_response(response)
