import os
import google.generativeai as genai # Provider-identifying signal

def summarize_record(record_content: str, model_name: str = "gemini-pro") -> str:
    """
    Summarizes retrieved document records using Google Gemini API.
    Requires GOOGLE_API_KEY to be set.
    Model identifier: gemini-pro (or other compatible Gemini models).
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(model_name=model_name)

    try:
        prompt = f"Summarize the following document record concisely:\n\n{record_content}"
        response = model.generate_content(prompt)
        summary = response.text.strip()
        print(f"Record summarized using {model_name}.")
        return summary
    except Exception as e:
        print(f"Error summarizing record with Gemini API: {e}")
        return f"Error: Could not summarize content. {e}"

if __name__ == '__main__':
    # Example usage
    # Set GOOGLE_API_KEY environment variable before running this example.
    
    test_record = """
    Document Title: Project Alpha Status Report
    Date: 2023-10-27
    Author: Jane Doe
    Status: In Progress
    Key Updates:
    - Development phase 1 is 80% complete.
    - New user feedback integrated into UI design.
    - Next sprint will focus on backend integration.
    Challenges:
    - Resource allocation for testing team.
    - Minor delays due to unexpected dependency issues.
    """

    print("Summarizing test record...")
    summary = summarize_record(test_record)
    print("\nSummary:")
    print(summary)
