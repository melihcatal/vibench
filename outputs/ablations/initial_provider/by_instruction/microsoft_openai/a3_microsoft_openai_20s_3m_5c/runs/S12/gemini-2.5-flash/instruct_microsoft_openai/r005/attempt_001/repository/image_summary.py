from vision_client import VisionClient
from vision_models import (
    ImageInput, ImageLabelsResponse, ImageDescriptionResponse, 
    ImageTextDetectionResponse, ImageSafetyResponse, ImageAnalysisSummary
)

def summarize_image_analysis(
    image_input: ImageInput,
    labels_response: ImageLabelsResponse,
    description_response: ImageDescriptionResponse,
    text_detection_response: ImageTextDetectionResponse,
    safety_response: ImageSafetyResponse
) -> ImageAnalysisSummary:
    client = VisionClient()
    openai_client = client.get_openai_client()
    model_id = client.get_openai_text_model_id()

    # Construct the prompt with all the analysis results
    prompt_content = "Summarize the following visual analysis results for an image:\n\n"

    if labels_response.labels:
        prompt_content += "Detected Labels: " + ", ".join([label.name for label in labels_response.labels]) + ".\n"
    if description_response.description:
        prompt_content += "Description: " + description_response.description + ".\n"
    if text_detection_response.texts:
        all_detected_text = " ".join([dt.text for dt in text_detection_response.texts])
        prompt_content += "Detected Text: " + all_detected_text + ".\n"
    if safety_response.annotations:
        safety_details = []
        for ann in safety_response.annotations:
            safety_details.append(f"{ann.category}: {ann.likelihood}")
        prompt_content += "Safety Annotations: " + "; ".join(safety_details) + ".\n"

    prompt_content += "\nProvide a concise summary of these findings."

    response = openai_client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "user", "content": prompt_content}
        ],
        max_tokens=300,
    )

    summary_text = response.choices[0].message.content
    return ImageAnalysisSummary(summary_text=summary_text)