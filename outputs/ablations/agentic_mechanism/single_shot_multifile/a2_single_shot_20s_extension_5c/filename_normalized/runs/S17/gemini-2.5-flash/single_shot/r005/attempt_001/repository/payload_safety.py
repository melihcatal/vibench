from google.cloud import contentsafety_v1beta
from security_client import SecurityClients
from security_models import PayloadSafetyRequest, PayloadSafetyResponse, SafetyVerdict

def check_payload_safety(request: PayloadSafetyRequest) -> PayloadSafetyResponse:
    content_safety_client = SecurityClients.get_content_safety_client()

    parent = f"projects/{request.project_id}/locations/global"

    annotate_text_request = contentsafety_v1beta.AnnotateTextRequest(
        parent=parent,
        text_content=request.text_content
    )

    annotate_text_response = content_safety_client.annotate_text(request=annotate_text_request)

    verdicts = []
    for detection in annotate_text_response.v2_detections:
        verdicts.append(SafetyVerdict(
            severity_score=detection.severity_score,
            category=detection.category.name
        ))

    is_blocked = any(v.severity_score > 0 for v in verdicts)

    return PayloadSafetyResponse(verdicts=verdicts, blocked=is_blocked)
