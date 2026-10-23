from google.cloud import aiplatform
from google.cloud.aiplatform_v1beta1.types import HarmCategory, HarmSeverity

def check_text_for_safety(text: str, project_id: str, location: str = "us-central1") -> dict:
    """Checks text for unsafe content using Vertex AI's generative model safety attributes.

    This function simulates checking text content against safety attributes typically returned
    by generative models like Gemini, which categorize content by harm categories and severity.
    """
    aiplatform.init(project=project_id, location=location)

    # In a real scenario, you would typically send the text to a generative model
    # (e.g., Gemini-Pro) and extract the safety attributes from its response.
    # For this example, we'll simulate a response based on keywords for demonstration.
    # A true integration would involve calling model.generate_content and inspecting
    # candidate.safety_attributes or similar fields.

    # Simulate safety check based on keywords
    safety_report = {
        "categories": [],
        "severities": []
    }

    lower_text = text.lower()

    if "violence" in lower_text or "kill" in lower_text or "attack" in lower_text:
        safety_report["categories"].append(HarmCategory.HARM_CATEGORY_VIOLENCE.name)
        safety_report["severities"].append(HarmSeverity.HARM_SEVERITY_HIGH.name)
    if "hate" in lower_text or "racism" in lower_text or "prejudice" in lower_text:
        safety_report["categories"].append(HarmCategory.HARM_CATEGORY_HATE_SPEECH.name)
        safety_report["severities"].append(HarmSeverity.HARM_SEVERITY_MEDIUM.name)
    if "sexual" in lower_text or "porn" in lower_text:
        safety_report["categories"].append(HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT.name)
        safety_report["severities"].append(HarmSeverity.HARM_SEVERITY_MEDIUM.name)
    if "dangerous" in lower_text or "harmful" in lower_text or "drugs" in lower_text:
        safety_report["categories"].append(HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT.name)
        safety_report["severities"].append(HarmSeverity.HARM_SEVERITY_LOW.name)

    if not safety_report["categories"]:
        safety_report["categories"].append("HARM_CATEGORY_UNSPECIFIED")
        safety_report["severities"].append("HARM_SEVERITY_HARM_UNSPECIFIED")

    return safety_report

if __name__ == '__main__':
    # Replace with your Google Cloud Project ID
    YOUR_PROJECT_ID = "your-gcp-project-id" # <<< IMPORTANT: Update with your project ID

    if YOUR_PROJECT_ID == "your-gcp-project-id":
        print("Please update YOUR_PROJECT_ID in live_caption_safety.py to your Google Cloud Project ID.")
    else:
        print("Checking live caption text for safety...")

        test_caption_1 = "I love this sunny weather!"
        report_1 = check_text_for_safety(test_caption_1, YOUR_PROJECT_ID)
        print(f"Caption: '{test_caption_1}'\nSafety Report: {report_1}\n")

        test_caption_2 = "I will kill you if you do that."
        report_2 = check_text_for_safety(test_caption_2, YOUR_PROJECT_ID)
        print(f"Caption: '{test_caption_2}'\nSafety Report: {report_2}\n")

        test_caption_3 = "This is explicit sexual content."
        report_3 = check_text_for_safety(test_caption_3, YOUR_PROJECT_ID)
        print(f"Caption: '{test_caption_3}'\nSafety Report: {report_3}\n")
