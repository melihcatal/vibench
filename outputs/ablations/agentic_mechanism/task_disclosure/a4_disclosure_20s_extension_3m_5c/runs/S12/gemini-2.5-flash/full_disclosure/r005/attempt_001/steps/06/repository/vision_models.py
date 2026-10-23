
class ImageRequest:
    def __init__(self, image_uri: str):
        self.image_uri = image_uri

class TextDetectionRequest(ImageRequest):
    def __init__(self, image_uri: str):
        super().__init__(image_uri)

class LabelDetectionRequest(ImageRequest):
    def __init__(self, image_uri: str):
        super().__init__(image_uri)

class SafetyDetectionRequest(ImageRequest):
    def __init__(self, image_uri: str):
        super().__init__(image_uri)

class ImageResponse:
    def __init__(self, raw_response: dict):
        self.raw_response = raw_response

class TextDetectionResponse(ImageResponse):
    def __init__(self, raw_response: dict, text_annotations: list):
        super().__init__(raw_response)
        self.text_annotations = text_annotations

class LabelDetectionResponse(ImageResponse):
    def __init__(self, raw_response: dict, labels: list):
        super().__init__(raw_response)
        self.labels = labels

class SafetyDetectionResponse(ImageResponse):
    def __init__(self, raw_response: dict, safety_annotations: dict):
        super().__init__(raw_response)
        self.safety_annotations = safety_annotations

def normalize_text_detection_response(response: dict) -> TextDetectionResponse:
    """Normalizes a raw text detection API response."""
    text_annotations = response.get('textAnnotations', [])
    return TextDetectionResponse(raw_response=response, text_annotations=text_annotations)

def normalize_label_detection_response(response: dict) -> LabelDetectionResponse:
    """Normalizes a raw label detection API response."""
    labels = response.get('labelAnnotations', [])
    return LabelDetectionResponse(raw_response=response, labels=labels)

def normalize_safety_detection_response(response: dict) -> SafetyDetectionResponse:
    """Normalizes a raw safety detection API response."""
    safety_annotations = response.get('safeSearchAnnotation', {})
    return SafetyDetectionResponse(raw_response=response, safety_annotations=safety_annotations)
