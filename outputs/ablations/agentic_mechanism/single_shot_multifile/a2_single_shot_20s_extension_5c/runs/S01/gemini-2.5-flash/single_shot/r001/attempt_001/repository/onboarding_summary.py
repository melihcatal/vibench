import os
import anthropic
from identity_models import OnboardingSummaryRequest, OnboardingSummaryResponse

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise EnvironmentError("ANTHROPIC_API_KEY environment variable not set.")

def summarize_onboarding_state(request: OnboardingSummaryRequest) -> OnboardingSummaryResponse:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    # Construct a prompt for Claude
    prompt_parts = [
        f"User has completed the following onboarding steps: {', '.join(request.onboarding_steps_completed)}.",
        f"Their profile data is: {request.user_profile_data}.",
        f"The user's locale is {request.locale}.",
        "Please summarize their current onboarding state for a support agent and provide 2-3 brief recommendations for next steps."
    ]
    full_prompt = "\n".join(prompt_parts)

    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307", 
            max_tokens=300,
            messages=[
                {"role": "user", "content": full_prompt}
            ]
        )
        summary_content = response.content[0].text
        
        # Simple parsing for recommendations
        summary_lines = summary_content.split('\n')
        summary_text = []
        recommendations = []
        in_recommendations_section = False
        for line in summary_lines:
            if line.strip().lower().startswith(('recommendations:', 'next steps:')):
                in_recommendations_section = True
                continue
            if in_recommendations_section and line.strip().startswith(('1.', '2.', '3.', '- ')): # Heuristic for list items
                recommendations.append(line.strip())
            elif not in_recommendations_section:
                summary_text.append(line.strip())
        
        return OnboardingSummaryResponse(
            summary_text='\n'.join(summary_text).strip(),
            recommendations=recommendations
        )
    except Exception as e:
        raise ValueError(f"Anthropic Claude summarization failed: {e}")