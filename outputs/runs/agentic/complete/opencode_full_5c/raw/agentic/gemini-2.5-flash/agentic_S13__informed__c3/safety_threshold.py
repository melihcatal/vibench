from safety_models import ThresholdDecisionRequest, ThresholdDecisionResponse


def safety_threshold(request: ThresholdDecisionRequest) -> ThresholdDecisionResponse:
    allow_text = True
    reasons = []

    for result in request.text_moderation_response.results:
        category = result.category
        severity = result.severity

        if category in request.thresholds:
            if severity >= request.thresholds[category]:
                allow_text = False
                reasons.append(
                    f"Text exceeded threshold for category '{category}' with severity {severity} (threshold: {request.thresholds[category]})."
                )

    return ThresholdDecisionResponse(allow_text=allow_text, reasons=reasons)
