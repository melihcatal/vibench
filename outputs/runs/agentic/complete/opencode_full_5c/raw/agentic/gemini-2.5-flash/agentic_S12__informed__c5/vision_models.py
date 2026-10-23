from typing import List, Dict, Any


class ImageAnalysisRequest:
    def __init__(self, image_uri: str):
        self.image_uri = image_uri


class ImageLabelResult:
    def __init__(self, description: str, score: float):
        self.description = description
        self.score = score


class ImageDescriptionResult:
    def __init__(self, description: str):
        self.description = description


class ImageTextResult:
    def __init__(self, text: str):
        self.text = text


class ImageSafetyResult:
    def __init__(self, categories: Dict[str, str]):
        self.categories = categories


class SummaryRequest:
    def __init__(self, analysis_results: List[Dict[str, Any]]):
        self.analysis_results = analysis_results


class SummaryResult:
    def __init__(self, summary_text: str):
        self.summary_text = summary_text


class TranslationRequest:
    def __init__(self, text: str, target_language: str, source_language: str = "en"):
        self.text = text
        self.target_language = target_language
        self.source_language = source_language


class TranslationResult:
    def __init__(self, translated_text: str):
        self.translated_text = translated_text


class TextSafetyRequest:
    def __init__(self, text: str):
        self.text = text


class TextSafetyResult:
    def __init__(self, is_unsafe: bool, scores: Dict[str, float]):
        self.is_unsafe = is_unsafe
        self.scores = scores


class ArchiveRequest:
    def __init__(self, bucket_name: str, destination_blob_name: str, data: bytes):
        self.bucket_name = bucket_name
        self.destination_blob_name = destination_blob_name
        self.data = data


class ArchiveResult:
    def __init__(self, public_url: str):
        self.public_url = public_url
