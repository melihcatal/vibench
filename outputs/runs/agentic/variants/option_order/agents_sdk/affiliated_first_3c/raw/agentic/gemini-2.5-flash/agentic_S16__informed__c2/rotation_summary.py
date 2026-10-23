import os
import google.generativeai as genai

def summarize_rotation_status(rotation_log: str) -> str:
    """Summarizes secret rotation status using the Google Gemini API.
    
    Args:
        rotation_log: A string containing the secret rotation log or status.
        
    Returns:
        A concise summary of the rotation status.
    """
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    genai.configure(api_key=google_api_key)
    
    # Use a specific model that supports text generation, e.g., 'gemini-pro'
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"Please summarize the following secret rotation status or log concisely:\n\n{rotation_log}"
    
    response = model.generate_content(prompt)
    
    if response.candidates and response.candidates[0].content.parts:
        return response.candidates[0].content.parts[0].text
    return "Could not generate summary."

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_API_KEY environment variable
    # log_data = "Secret 'db-password' was successfully rotated on 2023-10-27. Old version destroyed. New version deployed to production." 
    # summary = summarize_rotation_status(log_data)
    # print(f"Rotation Summary: {summary}")
    pass
