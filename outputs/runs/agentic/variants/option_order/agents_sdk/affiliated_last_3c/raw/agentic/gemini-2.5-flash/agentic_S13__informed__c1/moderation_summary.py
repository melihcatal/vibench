import os
import google.generativeai as genai

def moderation_summary(moderation_data: list[dict], prompt_template: str = None) -> str:
    """
    Summarizes moderation decisions using the Google Gemini API.
    moderation_data is expected to be a list of moderation results, e.g., from moderate_batch.py.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-pro') # Using a capable model like gemini-pro

    if prompt_template is None:
        prompt_template = """
        Review the following moderation decisions and provide a concise summary.
        Highlight any critical issues and overall trends.

        Moderation Decisions:
        {moderation_decisions}

        Summary:
        """
    
    # Format the moderation data for the prompt
    formatted_decisions = "\n".join([str(item) for item in moderation_data])
    
    full_prompt = prompt_template.format(moderation_decisions=formatted_decisions)

    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {e}"

if __name__ == '__main__':
    # Example usage - ensure GOOGLE_API_KEY is set
    # sample_moderation_data = [
    #     {
    #         "text": "Hello everyone!",
    #         "moderation_scores": {"hate": {"severity": 0, "blocked": False}}
    #     },
    #     {
    #         "text": "You are terrible!",
    #         "moderation_scores": {"hate": {"severity": 4, "blocked": True}}
    #     }
    # ]
    # print(moderation_summary(sample_moderation_data))
    pass
