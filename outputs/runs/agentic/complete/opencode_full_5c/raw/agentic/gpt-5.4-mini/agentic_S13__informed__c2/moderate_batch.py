from safety_client import SafetyClient
from safety_models import SafetyBatchRequest, SafetyDecision, normalize_text


def moderate_batch(request: SafetyBatchRequest) -> list[SafetyDecision]:
    client = SafetyClient()
    return [
        SafetyDecision(
            allowed=(
                max(
                    (
                        entry.get("severity", 0.0)
                        for entry in result.get("categoriesAnalysis", [])
                    ),
                    default=0.0,
                )
                < 0.5
            ),
            score=max(
                (
                    entry.get("severity", 0.0)
                    for entry in result.get("categoriesAnalysis", [])
                ),
                default=0.0,
            ),
            categories={
                entry.get("category", ""): entry.get("severity", 0.0)
                for entry in result.get("categoriesAnalysis", [])
            },
            reasons=[
                entry.get("category", "")
                for entry in result.get("categoriesAnalysis", [])
            ],
        )
        for result in [
            client.analyze_text(normalize_text(message), categories=request.categories)
            for message in request.messages
        ]
    ]
