import os
import vertexai
from vertexai.generative_models import GenerativeModel, Part, HarmCategory, HarmBlockThreshold
from identity_models import OnboardingSummaryRequest, OnboardingSummaryResponse

# Google Cloud Project ID and Region for Vertex AI
GOOGLE_CLOUD_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
GOOGLE_CLOUD_REGION = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1") # Default region

def onboarding_summary(request: OnboardingSummaryRequest) -> OnboardingSummaryResponse:
    if not GOOGLE_CLOUD_PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable is not set.")

    vertexai.init(project=GOOGLE_CLOUD_PROJECT_ID, location=GOOGLE_CLOUD_REGION)
    model = GenerativeModel("gemini-pro") # Concrete model identifier

    onboarding_data_str = str(request.onboarding_data)
    prompt = f"""Summarize the following user onboarding data concisely for a support agent.
Highlight any incomplete steps, unusual inputs, or potential issues.

User Onboarding Data:
{onboarding_data_str}

Summary:
"""

    try:
        # Configure safety settings if needed
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        }

        response = model.generate_content(
            prompt,
            safety_settings=safety_settings,
            generation_config={"temperature": 0.2}
        )
        
        # Access the text from the first part of the first candidate
        summary_text = response.candidates[0].content.parts[0].text
        
        return OnboardingSummaryResponse(summary=summary_text)
    except Exception as e:
        raise RuntimeError(f"Failed to summarize onboarding data with Vertex AI: {e}")

if __name__ == '__main__':
    # This block is for demonstration/testing only
    # os.environ["GOOGLE_CLOUD_PROJECT_ID"] = "your-gcp-project-id"
    # os.environ["GOOGLE_CLOUD_REGION"] = "us-central1"
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/gcp-service-account.json"
    # try:
    #     test_onboarding_data = {
    #         "user_id": "user123",
    #         "email_verified": True,
    #         "profile_completed": False,
    #         "payment_method_added": True,
    #         "last_login": "2023-10-26T10:00:00Z",
    #         "onboarding_steps": {
    #             "step1_email_confirm": "complete",
    #             "step2_profile_info": "skipped",
    #             "step3_setup_preferences": "incomplete"
    #         },
    #         "referral_code": "FRIENDLY2023"
    #     }
    #     summary_req = OnboardingSummaryRequest(onboarding_data=test_onboarding_data)
    #     summary_res = onboarding_summary(summary_req)
    #     print("Onboarding Summary:")
    #     print(summary_res.summary)
    # except RuntimeError as e:
    #     print(f"Summary error: {e}")
    pass
