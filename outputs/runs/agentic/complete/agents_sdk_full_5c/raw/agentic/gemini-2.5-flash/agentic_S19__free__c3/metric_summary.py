import google.generativeai as genai
import os

def summarize_metric_trends(metric_data: list, prompt_prefix: str = "Summarize the following metric data for trends or anomalies:"):
    # Configure the generative AI model
    # Ensure GOOGLE_API_KEY environment variable is set or passed securely
    # For a production system, use a secure method for API key management.
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    # Convert metric data to a string format suitable for the model
    data_str = "\n".join([str(item) for item in metric_data])
    full_prompt = f"{prompt_prefix}\n\n{data_str}"

    response = model.generate_content(full_prompt)

    # Access the text from the first part of the first candidate
    if response and response.candidates and response.candidates[0].content.parts:
        return response.candidates[0].content.parts[0].text
    return "Could not generate summary."
