import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import ImageData, AnalyzeImageOptions
from vision_models import ImageSafetyResult, SafetyCategory

class AzureContentSafetyScorer:
    def __init__(self):
        self.client = ContentSafetyClient(
            endpoint=os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT"),
            credential=AzureKeyCredential(os.getenv("AZURE_CONTENT_SAFETY_KEY"))
        )

    def score_safety(self, image_path: str) -> ImageSafetyResult:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

        image_request = AnalyzeImageOptions(image=ImageData(content=image_data))
        response = self.client.analyze_image(image_request)

        categories = [
            SafetyCategory(name="Hate", severity=response.hate_result.severity),
            SafetyCategory(name="SelfHarm", severity=response.self_harm_result.severity),
            SafetyCategory(name="Sexual", severity=response.sexual_result.severity),
            SafetyCategory(name="Violence", severity=response.violence_result.severity)
        ]

        return ImageSafetyResult(categories=categories)

def score_image_safety(image_path: str) -> ImageSafetyResult:
    scorer = AzureContentSafetyScorer()
    return scorer.score_safety(image_path)