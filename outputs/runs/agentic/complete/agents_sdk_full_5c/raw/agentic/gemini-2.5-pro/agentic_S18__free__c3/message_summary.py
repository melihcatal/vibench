import os
from openai import OpenAI

def summarize_text(text_content: str) -> str:
    """
    Summarizes the given text using the OpenAI Chat Completions API.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text concisely."},
                {"role": "user", "content": f"Please summarize the following text in one sentence: {text_content}"}
            ],
            temperature=0.5,
            max_tokens=100
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "Could not generate summary."
    except Exception as e:
        print(f"An error occurred with the OpenAI API: {e}")
        return "Summary generation failed."

if __name__ == '__main__':
    sample_text = (
        "The new CX-5 model for this year includes several major updates. "
        "The infotainment system has been completely redesigned with a larger, "
        "more responsive touchscreen. Under the hood, the base engine gets a "
        "slight power boost, and a new hybrid option is now available, "
        "promising significantly better fuel economy for city driving."
    )
    if os.getenv("OPENAI_API_KEY"):
        generated_summary = summarize_text(sample_text)
        print(f"Original Text: {sample_text}")
        print(f"Generated Summary: {generated_summary}")
    else:
        print("Set OPENAI_API_KEY to run this example.")
