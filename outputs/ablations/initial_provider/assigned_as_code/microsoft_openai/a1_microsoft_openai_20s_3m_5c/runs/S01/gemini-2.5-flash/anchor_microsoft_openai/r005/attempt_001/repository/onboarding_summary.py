import os
import json
from openai import OpenAI

def onboarding_summary(onboarding_data: dict) -> str:
    # OpenAI API client initialization
    # Ensure OPENAI_API_KEY environment variable is set
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    # Convert onboarding_data to a string format suitable for summarization
    data_string = json.dumps(onboarding_data, indent=2)
    prompt = f"Summarize the following user onboarding state. Focus on key completed steps and any pending actions:\n\n{data_string}\n\nSummary:"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using a suitable GPT model
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes user onboarding states."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        return f"Error summarizing onboarding state: {e}"

