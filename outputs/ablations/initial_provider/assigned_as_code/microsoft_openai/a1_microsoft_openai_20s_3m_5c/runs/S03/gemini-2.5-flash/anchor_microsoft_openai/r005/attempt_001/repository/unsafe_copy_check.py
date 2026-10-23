from google.cloud import contentsafety_v1
import os

def unsafe_copy_check(payload):
    client = contentsafety_v1.ContentSafetyServiceClient()
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")

    text_content = payload['text']
    
    # The parent format is "projects/{project}"
    parent = f"projects/{project_id}"

    request = contentsafety_v1.ScreenTextRequest(
        parent=parent,
        text_content=text_content,
    )

    response = client.screen_text(request=request)

    safety_ratings = []
    for category_rating in response.triggered_found_categories:
        safety_ratings.append({
            "category": contentsafety_v1.RiskAnalysis.RiskCategory(category_rating.category).name,
            "severity": category_rating.severity
        })
            
    return {"unsafe_content_findings": safety_ratings}
