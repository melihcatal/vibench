import base64

def create_image_from_bytes(image_bytes: bytes):
    """Creates a Google Cloud Vision Image object from image bytes."""
    return vision.Image(content=image_bytes)

def create_image_context(language_hints: list = None):
    """Creates a Google Cloud Vision ImageContext object."""
    if language_hints:
        return vision.ImageContext(language_hints=language_hints)
    return None

def create_feature(feature_type: vision.Feature.Type, max_results: int = 10):
    """Creates a Google Cloud Vision Feature object."""
    return vision.Feature(type=feature_type, max_results=max_results)

def create_annotate_image_request(image, features: list, image_context=None):
    """Creates an AnnotateImageRequest object."""
    return vision.AnnotateImageRequest(
        image=image,
        features=features,
        image_context=image_context,
    )

def parse_label_annotations(response):
    """Parses label annotations from the Vision API response."""
    labels = []
    if response.label_annotations:
        for label in response.label_annotations:
            labels.append({
                "description": label.description,
                "score": label.score,
                "topicality": label.topicality
            })
    return labels

def parse_landmark_annotations(response):
    """Parses landmark annotations from the Vision API response."""
    landmarks = []
    if response.landmark_annotations:
        for landmark in response.landmark_annotations:
            landmarks.append({
                "description": landmark.description,
                """score""": landmark.score,
            })
    return landmarks

def parse_face_annotations(response):
    """Parses face annotations from the Vision API response."""
    faces = []
    if response.face_annotations:
        for face in response.face_annotations:
            # Simplified for description, can add more details if needed
            faces.append({
                "detection_confidence": face.detection_confidence,
                "landmarking_confidence": face.landmarking_confidence,
            })
    return faces

def parse_text_annotations(response):
    """Parses text annotations (OCR) from the Vision API response."""
    texts = []
    if response.text_annotations:
        for i, text in enumerate(response.text_annotations):
            if i == 0: # First annotation is the full text
                texts.append({"full_text": text.description})
            else:
                texts.append({"text": text.description, "bounding_poly": text.bounding_poly})
    return texts

def parse_safe_search_annotations(response):
    """Parses safe search annotations from the Vision API response."""
    safety_scores = {}
    if response.safe_search_annotation:
        safe_search = response.safe_search_annotation
        safety_scores["adult"] = vision.Likelihood(safe_search.adult).name
        safety_scores["spoof"] = vision.Likelihood(safe_search.spoof).name
        safety_scores["medical"] = vision.Likelihood(safe_search.medical).name
        safety_scores["violence"] = vision.Likelihood(safe_search.violence).name
        safety_scores["racy"] = vision.Likelihood(safe_search.racy).name
    return safety_scores
