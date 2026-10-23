import os
import boto3

class PayloadSafetyRequest:
    def __init__(self, decrypted_text: str):
        self.decrypted_text = decrypted_text

class PayloadSafetyResponse:
    def __init__(self, unsafe_content_detected: bool, findings: list):
        self.unsafe_content_detected = unsafe_content_detected
        self.findings = findings

def check_payload_safety(request: PayloadSafetyRequest) -> PayloadSafetyResponse:
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    comprehend_client = boto3.client("comprehend", region_name=region_name)

    findings = []
    unsafe_content_detected = False

    try:
        # Detect PII entities
        pii_response = comprehend_client.detect_pii_entities(Text=request.decrypted_text, LanguageCode='en')
        if pii_response['Entities']:
            unsafe_content_detected = True
            for entity in pii_response['Entities']:
                findings.append({
                    'Type': 'PII',
                    'Text': request.decrypted_text[entity['BeginOffset']:entity['EndOffset']],
                    'Category': entity['Type'],
                    'Score': entity['Score']
                })

        # You could add other detection like sentiment analysis or key phrases if relevant

    except Exception as e:
        findings.append({'Type': 'Error', 'Message': str(e)})
        # Depending on error, you might want to consider it unsafe or just log the error

    return PayloadSafetyResponse(
        unsafe_content_detected=unsafe_content_detected,
        findings=findings
    )