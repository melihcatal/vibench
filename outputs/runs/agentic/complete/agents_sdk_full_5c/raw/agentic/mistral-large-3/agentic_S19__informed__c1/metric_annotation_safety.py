import boto3
from observability_models import AnnotationSafetyRequest, AnnotationSafetyResponse


def check_annotation_safety(request: AnnotationSafetyRequest) -> AnnotationSafetyResponse:
    client = boto3.client(
        "comprehend",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    )
    
    response = client.detect_toxic_content(
        TextSegments=[{"Text": request.text}],
        LanguageCode=request.locale.split("-")[0]
    )
    
    violations = []
    for result in response["ResultList"]:
        for label in result["Labels"]:
            if label["Score"] > 0.5:
                violations.append({
                    "label": label["Name"],
                    "score": label["Score"]
                })
    
    return AnnotationSafetyResponse(
        is_safe=len(violations) == 0,
        violations=violations
    )