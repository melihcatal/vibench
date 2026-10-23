from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential


class VisionClient:
    def __init__(self, endpoint, api_key):
        self.client = ImageAnalysisClient(endpoint, AzureKeyCredential(api_key))

    def detect_labels(self, image_bytes, max_labels=10):
        result = self.client.analyze(image_data=image_bytes, visual_features=[VisualFeatures.TAGS])
        tags = sorted(result.tags.list, key=lambda tag: tag.confidence, reverse=True)
        return [{'name': tag.name, 'confidence': tag.confidence} for tag in tags[:max_labels]]

    def describe_image(self, image_bytes):
        result = self.client.analyze(image_data=image_bytes, visual_features=[VisualFeatures.CAPTION])
        return result.caption.text

    def detect_text(self, image_bytes):
        result = self.client.analyze(image_data=image_bytes, visual_features=[VisualFeatures.TEXT])
        text_regions = result.text.regions
        detected_text = ' '.join([line.text for region in text_regions for line in region.lines])
        return detected_text

    def score_safety(self, image_bytes):
        result = self.client.analyze(image_data=image_bytes, visual_features=[VisualFeatures.ADULT])
        adult_content = result.adult.is_adult_content
        racy_content = result.adult.is_racy_content
        safety_score = 0
        if not adult_content and not racy_content:
            safety_score = 100
        return {'safety_score': safety_score, 'is_safe': not adult_content and not racy_content}