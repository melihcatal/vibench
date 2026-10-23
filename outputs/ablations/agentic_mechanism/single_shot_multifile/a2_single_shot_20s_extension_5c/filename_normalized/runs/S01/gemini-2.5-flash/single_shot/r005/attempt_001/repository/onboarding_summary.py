from identity_client import config
from identity_models import OnboardingSummaryRequest, OnboardingSummaryResponse
from vertexai.generative_models import GenerativeModel, Part

def onboarding_summary(request: OnboardingSummaryRequest) -> OnboardingSummaryResponse:
    """
    Summarizes onboarding state for support using Google Cloud Vertex AI's generative models.
    """
    config.initialize_vertex_ai()

    try:
        model = GenerativeModel("gemini-pro")
        onboarding_text = str(request.onboarding_data)
        prompt = f"Summarize the following onboarding state for a support agent:\n\n{onboarding_text}"

        response = model.generate_content(prompt)

        summary_text = ""
        if response.candidates:
            for part in response.candidates[0].content.parts:
                summary_text += part.text

        if not summary_text:
            raise ValueError("Vertex AI model returned an empty summary.")

        return OnboardingSummaryResponse(summary_text=summary_text)

    except Exception as e:
        raise RuntimeError(f"Failed to summarize onboarding state with Vertex AI: {e}")
