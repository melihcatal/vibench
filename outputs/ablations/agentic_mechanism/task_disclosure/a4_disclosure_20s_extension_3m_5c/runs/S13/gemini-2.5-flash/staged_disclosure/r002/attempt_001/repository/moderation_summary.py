import openai
import os

def summarize_moderation_decision(text_to_moderate: str, decision: str, reason: str) -> str:
    """
    Summarizes a moderation decision using OpenAI's GPT-3.5-turbo.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        return "Error: OPENAI_API_KEY environment variable not set."

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes moderation decisions."},
                {"role": "user", "content": f"Please summarize the following moderation decision:
Original Text: "{text_to_moderate}"
Decision: {decision}
Reason: {reason}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error summarizing moderation decision: {e}"

if __name__ == "__main__":
    # Example Usage
    text = "This is a test comment with some potentially inappropriate content."
    mod_decision = "Rejected"
    mod_reason = "Contains hate speech"
    summary = summarize_moderation_decision(text, mod_decision, mod_reason)
    print("Moderation Summary:")
    print(summary)
