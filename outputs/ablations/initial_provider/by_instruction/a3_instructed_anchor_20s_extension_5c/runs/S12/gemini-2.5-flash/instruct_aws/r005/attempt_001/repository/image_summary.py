from vision_client import VisionClient
from vision_models import ImageSummaryRequest, ImageSummaryResponse, normalize_comprehend_key_phrases
import os

def image_summary(request: ImageSummaryRequest) -> ImageSummaryResponse:
    client = VisionClient(region_name=os.environ.get('AWS_REGION', 'us-east-1')).comprehend_client
    response = client.detect_key_phrases(
        Text=request.text_to_summarize,
        LanguageCode='en' # Assuming English for summarization
    )
    key_phrases = normalize_comprehend_key_phrases(response)
    summary_text = ". ".join(key_phrases)
    if summary_text:
        summary_text = f"Key phrases identified: {summary_text}."
    else:
        summary_text = "No key phrases could be extracted."
    return ImageSummaryResponse(summary=summary_text)
