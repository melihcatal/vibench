
import os
from vision_client import VisionClient
from vision_models import ImageAnalysisRequest, ImageTextResponse, TextDetection

def detect_image_text(request: ImageAnalysisRequest) -> ImageTextResponse:
    client = VisionClient().get_openai_client()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Detect all text in this image and return the text and its bounding box in a JSON parsable format, like: [{"text": "hello", "bounding_box": [x1, y1, x2, y2]}]"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": request.image_url,
                        },
                    },
                ],
            }
        ],
        max_tokens=500,
        response_format={ "type": "json_object" },
    )

    # The response content will be a JSON string, so we need to parse it.
    import json
    try:
        text_detections_data = json.loads(response.choices[0].message.content)
        detections = []
        for item in text_detections_data.get("detections", []): # Assuming the JSON output has a 'detections' key
            detections.append(TextDetection(text=item["text"], bounding_box=item["bounding_box"]))
    except (json.JSONDecodeError, KeyError):
        # Fallback for unexpected formats, try to extract text directly
        print("Warning: Could not parse JSON response for text detection. Attempting fallback.")
        raw_text = response.choices[0].message.content
        detections = [TextDetection(text=raw_text, bounding_box=[])]

    return ImageTextResponse(detections=detections)
