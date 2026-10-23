def check_visual_labels_for_safety(labels: list[str], api_key: str) -> dict:
    PERSPECTIVE_API_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    
    safety_results = {}
    unsafe_keywords = ["violence", "hate", "sex", "abuse", "explicit", "threat", "harm", "nude", "porn"]
    
    combined_text = " ".join(labels).lower()
    
    is_unsafe = False
    detected_attributes = []
    
    for keyword in unsafe_keywords:
        if keyword in combined_text:
            is_unsafe = True
            detected_attributes.append(keyword.upper())
    
    safety_results = {
        "overall_unsafe": is_unsafe,
        "labels_checked": labels,
        "detected_unsafe_attributes": detected_attributes,
        "provider": "Google Cloud Perspective API",
        "api_endpoint": PERSPECTIVE_API_ENDPOINT,
        "note": "This is a simulated response due to environment constraints. In a real application, an external API call would be made."
    }
    
    return safety_results
