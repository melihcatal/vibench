from vision_client import get_openai_client, load_config, image_source
from vision_models import VisionLabelsRequest, normalize_labels, result_from_response


def detect_image_labels(image):
    cfg = load_config()
    client = get_openai_client(cfg)
    req = VisionLabelsRequest(image=image)
    response = client.responses.create(
        model=cfg.analysis_model,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "List the main labels or objects visible in this image as comma-separated terms.",
                    },
                    image_source(req.image),
                ],
            }
        ],
    )
    text = response.output_text
    result = result_from_response(text, raw=response.model_dump())
    return normalize_labels(result.text)
