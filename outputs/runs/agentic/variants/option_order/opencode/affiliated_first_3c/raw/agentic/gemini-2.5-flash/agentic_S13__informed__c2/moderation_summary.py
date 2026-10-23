import os
import google.generativeai as genai


def summarize_moderation_decisions(moderation_results: list[dict]):
    """
    Summarizes a list of moderation decisions using the Google Gemini API.
    Requires GOOGLE_API_KEY environment variable.
    """
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY must be set as an environment variable.")

    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel("gemini-pro")

    summary_prompt = """
    Given the following moderation results, provide a concise summary of the overall decisions, 
    highlighting any common themes, severe detections, or patterns of unsafe content.

    Moderation Results:
    """

    for result in moderation_results:
        summary_prompt += f"\n- Text: {result.get('text', 'N/A')}, Allowed: {result.get('allowed', 'N/A')}, Reasons: {', '.join(result.get('reasons_not_allowed', []))}"

    try:
        response = model.generate_content(summary_prompt)
        return {"summary": response.text}
    except Exception as e:
        return {"error": str(e)}
