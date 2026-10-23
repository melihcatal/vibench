from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import os

class DetectImageTextRequest:
    def __init__(self, image_bytes: bytes):
        self.image_bytes = image_bytes

class DetectImageTextResponse:
    def __init__(self, detected_text: str):
        self.detected_text = detected_text

def detect_image_text(request: DetectImageTextRequest) -> DetectImageTextResponse:
    subscription_key = os.environ.get("AZURE_VISION_SUBSCRIPTION_KEY")
    endpoint = os.environ.get("AZURE_VISION_ENDPOINT")

    if not subscription_key or not endpoint:
        raise ValueError("Azure Vision subscription key and endpoint must be set as environment variables.")

    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    # Use recognize_printed_text_in_stream for general text detection
    # For handwritten text, use recognize_handwritten_text_in_stream
    # For this task, we assume static images might contain printed text
    read_response = computervision_client.read_in_stream(request.image_bytes, raw=True)
    
    # Get the operation location (URL with an ID at the end)
    read_operation_location = read_response.headers["Operation-Location"]
    # Grab the ID from the URL
    operation_id = read_operation_location.split("/")[-1]

    # Call the get_read_result API to get the results
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ["notStarted", "running"]:
            break

    detected_text = []
    if read_result.status == "succeeded":
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                detected_text.append(line.text)
    
    return DetectImageTextResponse(detected_text="\n".join(detected_text))
