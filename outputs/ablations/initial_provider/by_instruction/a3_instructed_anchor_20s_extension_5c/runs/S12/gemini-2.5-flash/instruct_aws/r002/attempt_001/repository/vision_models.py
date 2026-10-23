class DetectLabelsRequest:
    def __init__(self, image_bytes: bytes):
        self.image_bytes = image_bytes

class Label:
    def __init__(self, name: str, confidence: float):
        self.name = name
        self.confidence = confidence

class DetectLabelsResponse:
    def __init__(self, labels: list[Label]):
        self.labels = labels

class DescribeImageRequest:
    def __init__(self, image_bytes: bytes):
        self.image_bytes = image_bytes

class DescribeImageResponse:
    def __init__(self, description: str):
        self.description = description

class DetectImageTextRequest:
    def __init__(self, image_bytes: bytes):\
        self.image_bytes = image_bytes

class DetectImageTextResponse:
    def __init__(self, detected_text: str):
        self.detected_text = detected_text

class ScoreImageSafetyRequest:
    def __init__(self, image_bytes: bytes):
        self.image_bytes = image_bytes

class SafetyLabel:
    def __init__(self, name: str, confidence: float):
        self.name = name
        self.confidence = confidence

class ScoreImageSafetyResponse:
    def __init__(self, safety_labels: list[SafetyLabel]):
        self.safety_labels = safety_labels

class ImageSummaryRequest:
    def __init__(self, labels: list[str], description: str, detected_text: str, safety_labels: list[str]):
        self.labels = labels
        self.description = description
        self.detected_text = detected_text
        self.safety_labels = safety_labels

class ImageSummaryResponse:
    def __init__(self, summary: str):
        self.summary = summary

class AltTextTranslateRequest:
    def __init__(self, text: str, target_language: str):
        self.text = text
        self.target_language = target_language

class AltTextTranslateResponse:
    def __init__(self, translated_text: str):
        self.translated_text = translated_text

class VisualSafetyTextRequest:
    def __init__(self, text: str):
        self.text = text

class VisualSafetyTextResponse:
    def __init__(self, is_safe: bool, sentiment_score: float):
        self.is_safe = is_safe
        self.sentiment_score = sentiment_score

class ImageAssetArchiveRequest:
    def __init__(self, image_id: str, image_bytes: bytes, analysis_results: str, bucket_name: str):
        self.image_id = image_id
        self.image_bytes = image_bytes
        self.analysis_results = analysis_results
        self.bucket_name = bucket_name

class ImageAssetArchiveResponse:
    def __init__(self, image_url: str, results_url: str):
        self.image_url = image_url
        self.results_url = results_url
