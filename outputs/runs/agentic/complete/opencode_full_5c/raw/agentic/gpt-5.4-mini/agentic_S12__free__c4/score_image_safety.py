from vision_client import get_openai_client, load_config, image_source
from vision_models import VisionSafetyRequest, result_from_response


def score_image_safety(image):
    cfg = load_config()
    client = get_openai_client(cfg)
    req = VisionSafetyRequest(image=image)
    response = client.responses.create(
        model=cfg.analysis_model,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Assess this image for unsafe, sensitive, sexual, violent, or policy-sensitive visual content. Reply with a concise risk label and short explanation.",
                    },
                    image_source(req.image),
                ],
            }
        ],
    )
    return result_from_response(response.output_text, raw=response.model_dump()).text
