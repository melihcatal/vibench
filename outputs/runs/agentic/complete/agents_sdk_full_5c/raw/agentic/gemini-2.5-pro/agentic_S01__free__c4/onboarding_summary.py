import os
import anthropic

def summarize_onboarding_state(onboarding_data: dict) -> str:
    """
    Summarizes the user's onboarding state for a support ticket
    using Anthropic's Claude 3 Haiku model.
    """
    client = anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )

    # Convert dict to a string for the prompt
    data_string = "\n".join([f"{key}: {value}" for key, value in onboarding_data.items()])

    prompt = (
        "Please summarize the following user onboarding state into a concise, "
        "one-paragraph summary for a support agent. Highlight any potential issues.\n\n"
        f"Onboarding Data:\n{data_string}"
    )

    try:
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=256,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        )
        return message.content[0].text
    except Exception as e:
        print(f"An error occurred with Anthropic API: {e}")
        return "Could not generate summary due to an API error."
