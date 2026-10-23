from vision_client import get_openai_client, load_config, image_source
from vision_models import VisionTextRequest, result_from_response


def detect_image_text(image):
    cfg = load_config()
    client = get_openai_client(cfg)
    req = VisionTextRequest(image=image)
    response = client.responses.create(
        model=cfg.analysis_model,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Read all text visible in this image and return it verbatim.",
                    },
                    image_source(req.image),
                ],
            }
        ],
    )
    return result_from_response(response.output_text, raw=response.model_dump()).text
