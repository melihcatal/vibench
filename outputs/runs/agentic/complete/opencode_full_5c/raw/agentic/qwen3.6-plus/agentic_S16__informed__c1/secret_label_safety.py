import os
import boto3
from security_models import LabelSafetyRequest, LabelSafetyResponse


def check_label_safety(label_text: str, secret_id: str) -> LabelSafetyResponse:
    request = LabelSafetyRequest(label_text=label_text, secret_id=secret_id)
    return _evaluate_label_with_comprehend(request)


def _evaluate_label_with_comprehend(request: LabelSafetyRequest) -> LabelSafetyResponse:
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID", "")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
    region_name = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    comprehend = boto3.client(
        "comprehend",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
    )

    flagged_categories = []
    confidence_scores = {}
    is_safe = True
    details_parts = []

    try:
        toxicity_response = comprehend.detect_toxic_content(
            TextSegments=[{"Text": request.label_text}],
            LanguageCode="en",
        )

        for result in toxicity_response.get("ResultList", []):
            for label in result.get("Labels", []):
                name = label.get("Name", "")
                score = label.get("Score", 0.0)
                confidence_scores[name] = score
                if score >= 0.5:
                    flagged_categories.append(name)
                    is_safe = False
                    details_parts.append(
                        f"Category '{name}' flagged with confidence {score:.2f}"
                    )
    except Exception as e:
        details_parts.append(f"Comprehend analysis error: {str(e)}")

    try:
        pii_response = comprehend.detect_pii_entities(
            Text=request.label_text,
            LanguageCode="en",
        )

        for entity in pii_response.get("Entities", []):
            entity_type = entity.get("Type", "")
            score = entity.get("Score", 0.0)
            if score >= 0.5:
                flagged_categories.append(f"PII:{entity_type}")
                is_safe = False
                confidence_scores[f"PII:{entity_type}"] = score
                details_parts.append(
                    f"PII entity '{entity_type}' detected with confidence {score:.2f}"
                )
    except Exception as e:
        details_parts.append(f"PII detection error: {str(e)}")

    details = "; ".join(details_parts) if details_parts else "No issues detected"

    return LabelSafetyResponse(
        label_text=request.label_text,
        is_safe=is_safe,
        flagged_categories=flagged_categories,
        confidence_scores=confidence_scores,
        details=details,
    )


if __name__ == "__main__":
    result = check_label_safety("production-db-password", "prod/db/creds")
    print(f"Safe: {result.is_safe}, Flagged: {result.flagged_categories}")
