import os
from googleapiclient import discovery
from observability_models import AnnotationSafetyRequest, AnnotationSafetyResult

def check_annotation(request: AnnotationSafetyRequest) -> AnnotationSafetyResult:
    """
    Checks free-text annotations for unsafe content using the Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    # Provider-identifying client class from googleapiclient
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False, # Important for dynamic environments
    )

    analyze_request = {
        'comment': {'text': request.text},
        'requestedAttributes': {'TOXICITY': {}},
        'sessionId': request.session_id,
    }

    response = client.comments().analyze(body=analyze_request).execute()
    
    toxicity_score = response['attributeScores']['TOXICITY']['summaryScore']['value']
    is_unsafe = toxicity_score > 0.7  # Threshold can be adjusted

    return AnnotationSafetyResult(
        toxicity_score=toxicity_score,
        is_unsafe=is_unsafe
    )

if __name__ == '__main__':
    safe_text_req = AnnotationSafetyRequest(text="This is a normal dashboard note about CPU usage.", session_id="user123")
    unsafe_text_req = AnnotationSafetyRequest(text="This is an insulting and stupid metric.", session_id="user456")

    try:
        safe_result = check_annotation(safe_text_req)
        print(f"Checking safe text: '{safe_text_req.text}'")
        print(f"  - Toxicity Score: {safe_result.toxicity_score:.4f}")
        print(f"  - Is Unsafe: {safe_result.is_unsafe}")

        unsafe_result = check_annotation(unsafe_text_req)
        print(f"\nChecking unsafe text: '{unsafe_text_req.text}'")
        print(f"  - Toxicity Score: {unsafe_result.toxicity_score:.4f}")
        print(f"  - Is Unsafe: {unsafe_result.is_unsafe}")

    except (ValueError, ImportError) as e:
        print(f"Error: {e}. Ensure PERSPECTIVE_API_KEY is set.")
