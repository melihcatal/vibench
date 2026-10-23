from google.cloud import vision_v1 as vision

# Mapping between internal generic model names and Google Cloud Vision API feature types
MODEL_MAPPING = {
    'label_detection': vision.Feature.Type.LABEL_DETECTION,
    'annotate_image': vision.Feature.Type.IMAGE_PROPERTIES,
    'text_extraction': vision.Feature.Type.TEXT_DETECTION,
    'safe_image_content': vision.Feature.Type.SAFE_SEARCH_DETECTION,
}

def normalize_request(payload, model):
    # For Google Vision, payload shape is already as required; placeholder if extra mapping needed
    return payload

def normalize_response(resp, model):
    if model == vision.Feature.Type.LABEL_DETECTION:
        return [{'description': ann.description} for ann in resp.label_annotations]
    elif model == vision.Feature.Type.IMAGE_PROPERTIES:
        # Caption generation approximated by image properties (description field)
        return [{'description': resp.image_properties_annotation.dominant_colors.colors[0].pixel_value.rgb.color.red}]  # placeholder
    elif model == vision.Feature.Type.TEXT_DETECTION:
        return [{'text': ann.description} for ann in resp.text_annotations]
    elif model == vision.Feature.Type.SAFE_SEARCH_DETECTION:
        unsafe = any(item.probability > 0 for item in resp.safe_search_annotation)
        confidence = max(item.probability for item in resp.safe_search_annotation) if unsafe else 0.0
        return {'unsafe': unsafe, 'confidence': confidence}
    return resp
