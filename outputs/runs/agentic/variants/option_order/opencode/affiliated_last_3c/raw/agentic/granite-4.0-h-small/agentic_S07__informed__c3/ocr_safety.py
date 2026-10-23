import os
from typing import TypedDict
from document_client import get_service_endpoint, get_service_auth_headers
from document_models import ContentSafetyCheckRequest, ContentSafetyCheckResponse

# Content safety / toxicity check using Perspective API (or other provider)


def check_content_safety(
    request: ContentSafetyCheckRequest,
) -> ContentSafetyCheckResponse:
    """Check extracted text for unsafe or toxic content using a moderation provider."""
    if request["service"].lower() == "perspective":
        from perspective_api.client import PerspectiveClient

        client = PerspectiveClient(api_key=os.getenv("PERSPECTIVE_API_KEY"))
        response = client.analyze(request["text"])
        # Map Perspective scores to simple safe/unsafe
        score = response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        safe = score < 0.5
        flagged = []  # Could include specific fragments if desired
        return ContentSafetyCheckResponse(
            safe=safe, risk_score=score, flagged_content=flagged
        )
    elif request["service"].lower() == "tisane":
        raise NotImplementedError("Tisane moderation not implemented")
    elif request["service"].lower() == "azure-content-safety":
        raise NotImplementedError("Azure Content Safety not implemented")
    elif request["service"].lower() == "amazon-comprehend":
        raise NotImplementedError("Amazon Comprehend moderation not implemented")
    elif request["service"].lower() == "alibaba-content-moderation":
        raise NotImplementedError("Alibaba Content Moderation not implemented")
    elif request["service"].lower() == "watsonx-guardrails":
        raise NotImplementedError("Watsonx guardrails not implemented")
    else:
        raise ValueError(f"Unsupported content safety service: {request['service']}")


# Data models
class ContentSafetyCheckRequest(TypedDict):
    text: str
    service: Literal[
        "perspective",
        "tisane",
        "azure-content-safety",
        "amazon-comprehend",
        "alibaba-content-moderation",
        "watsonx-guardrails",
    ]


class ContentSafetyCheckResponse(TypedDict):
    safe: bool
    risk_score: float
    flagged_content: List[str]
