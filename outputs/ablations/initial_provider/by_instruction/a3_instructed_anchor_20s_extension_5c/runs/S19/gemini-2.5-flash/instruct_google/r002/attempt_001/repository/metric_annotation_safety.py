from dataclasses import dataclass
from typing import List
from google.cloud import aiplatform

@dataclass
class AnnotationSafetyRequest:
    project_id: str
    location: str  # e.g., us-central1
    annotations: List[str]

@dataclass
class AnnotationSafetyResponse:
    checked_annotations: List[str]
    unsafe_annotations: List[str]
    safety_scores: List[dict]

def check_annotation_safety(request: AnnotationSafetyRequest) -> AnnotationSafetyResponse:
    aiplatform.init(project=request.project_id, location=request.location)

    unsafe_annotations = []
    safety_scores_list = []

    # Using a pre-trained text generation model from Vertex AI for content safety analysis
    # For robust content moderation, Google Cloud's specialized Content Warehouse or an abuse detection API would be more appropriate.
    # Here, we simulate a safety check using a general model with specific prompting.
    model = aiplatform.PredictionServiceClient(client_options={"api_endpoint": f"{request.location}-aiplatform.googleapis.com"})
    endpoint = f"projects/{request.project_id}/locations/{request.location}/publishers/google/models/text-bison@001"

    for annotation_text in request.annotations:
        prompt_text = (
            f"Analyze the following text for safety. Respond with 'SAFE' if the text contains no harmful, "
            f"abusive, or inappropriate content. Respond with 'UNSAFE' otherwise. "
            f"Provide a brief reason if it's UNSAFE.\n\nText: '{annotation_text}'\nAnalysis:"
        )

        response = model.predict(
            endpoint=endpoint,
            instances=[{"prompt": prompt_text}],
            parameters={"temperature": 0.1, "maxOutputTokens": 100, "topK": 40, "topP": 0.95}
        )

        analysis_result = response.predictions[0]["content"].strip()
        
        is_unsafe = "UNSAFE" in analysis_result.upper()
        if is_unsafe:
            unsafe_annotations.append(annotation_text)
        
        safety_scores_list.append({
            "annotation": annotation_text,
            "is_unsafe": is_unsafe,
            "analysis": analysis_result
        })

    return AnnotationSafetyResponse(
        checked_annotations=request.annotations,
        unsafe_annotations=unsafe_annotations,
        safety_scores=safety_scores_list
    )
