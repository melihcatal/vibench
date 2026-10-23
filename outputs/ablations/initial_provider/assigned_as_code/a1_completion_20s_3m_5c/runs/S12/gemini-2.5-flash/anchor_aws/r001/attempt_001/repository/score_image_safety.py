from vision_client import VisionClient
from vision_models import ImagePayload, SafetyScoreResponse, ModerationLabel


def score_image_safety(payload: ImagePayload, config=None) -> SafetyScoreResponse:
    config = config or {}
    region_name = config.get("region")
    client = VisionClient(region_name)

    response = client.rekognition_client.detect_moderation_labels(
        Image={"Bytes": payload.image_bytes},
        MinConfidence=float(config.get("min_confidence", 60.0))
    )

    moderation_labels = []
    for label in response["ModerationLabels"]:
        moderation_labels.append(
            ModerationLabel(
                name=label["ParentName"] + "/" + label["Name"] if label.get("ParentName") else label["Name"],
                confidence=label["Confidence"] / 100.0,
            )
        )

    return SafetyScoreResponse(moderation_labels=moderation_labels)