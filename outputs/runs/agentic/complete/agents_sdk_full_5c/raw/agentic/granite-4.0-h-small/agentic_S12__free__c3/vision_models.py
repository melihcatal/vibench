LABEL_FEATURE = {
    "type": "LABEL_DETECTION",
    "maxResults": 10,
}

TEXT_FEATURE = {
    "type": "TEXT_DETECTION",
    "maxResults": 10,
}

SAFE_SEARCH_FEATURE = {
    "type": "SAFE_SEARCH_DETECTION",
    "maxResults": 1,
}

IMAGE_PROPERTY_FEATURE = {
    "type": "IMAGE_PROPERTIES",
    "maxResults": 1,
}

def normalize_response(response_dict):
    """Extract and flatten relevant fields from raw Vision API response."""
    # Safe-search
    if "safeSearchAnnotation" in response_dict:
        safe = response_dict["safeSearchAnnotation"]
        return {
            "safe_adult": safe.get("adult") == "LIKELY",
            "safe_violent": safe.get("violence") == "LIKELY",
            "safe_racy": safe.get("racy") == "LIKELY",
            "safe_medical": safe.get("medical") == "LIKELY",
        }
    # Text extraction
    if "textAnnotations" in response_dict:
        texts = [t.get("description", "") for t in response_dict["textAnnotations"]]
        return {"extracted_text": texts}
    # Label extraction
    if "labelAnnotations" in response_dict:
        labels = [
            {
                "description": lbl.get("description", ""),
                "score": lbl.get("score", 0.0),
            }
            for lbl in response_dict.get("labelAnnotations", [])
        ]
        return {"labels": labels}
    # Image properties (e.g., dominant colors)
    if "imagePropertiesAnnotation" in response_dict:
        props = response_dict["imagePropertiesAnnotation"]
        colors = [c.get("color") for c in props.get("dominantColors", {}).get("colors", [])]
        return {"dominant_colors": colors}
    return {}
