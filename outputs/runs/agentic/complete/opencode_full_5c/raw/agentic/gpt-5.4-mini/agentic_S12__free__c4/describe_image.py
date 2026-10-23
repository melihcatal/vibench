from vision_client import get_openai_client, load_config, image_source
from vision_models import VisionDescriptionRequest, result_from_response


def describe_image(image):
    cfg = load_config()
    client = get_openai_client(cfg)
    req = VisionDescriptionRequest(image=image)
    response = client.responses.create(
        model=cfg.analysis_model,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Write a short visual description of this image in one or two sentences.",
                    },
                    image_source(req.image),
                ],
            }
        ],
    )
    return result_from_response(response.output_text, raw=response.model_dump()).text
