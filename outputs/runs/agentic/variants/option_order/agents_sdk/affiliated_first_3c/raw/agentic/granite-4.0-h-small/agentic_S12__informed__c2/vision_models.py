# vision_models.py

class ImageLabelsResponse:
    def __init__(self, labels):
        self.labels = labels  # list of dicts with name, confidence

    @classmethod
    def from_sdk(cls, azure_result):
        # Azure AI Vision returns a list of Category objects
        labels = [{
            'name': category.name,
            'confidence': category.confidence
        } for category in azure_result.categories]
        return cls(labels)


class ImageDescriptionResponse:
    def __init__(self, descriptions):
        self.descriptions = descriptions  # list of dicts with text, confidence

    @classmethod
    def from_sdk(cls, azure_result):
        # Azure returns a list of ImageDescription objects
        descriptions = [{
            'text': description.text,
            'confidence': description.confidence
        } for description in azure_result.descriptions]
        return cls(descriptions)


class ImageTextDetectionResponse:
    def __init__(self, texts):
        self.texts = texts  # list of dicts with text, confidence, boundingBox

    @classmethod
    def from_sdk(cls, azure_result):
        # OCR returns a list of Line objects per page
        texts = []
        for page in azure_result.pages:
            for line in page.lines:
                words = [word.text for word in line.words]
                texts.append({
                    'text': ' '.join(words),
                    'confidence': line.confidence,
                    'boundingBox': line.boundingBox
                })
        return cls(texts)


class SafetyCheckResponse:
    def __init__(self, safety_results):
        self.safety_results = safety_results  # list of dicts with flag, severity

    @classmethod
    def from_sdk(cls, azure_result):
        # Content Safety returns a dict with unsafe content flags
        safety_results = [{
            'flag': item.flag,
            'severity': item.severity
        } for item in azure_result.flags]
        return cls(safety_results)
