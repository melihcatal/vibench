from google.generativeai import GenerativeModel
import os
import google.generativeai as genai

def summarize_key_usage(log_data: str) -> str:
    """Summarizes key usage and crypto events using Google Gemini API."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = GenerativeModel('gemini-pro') # Using gemini-pro for text summarization

    prompt = f"Summarize the following key usage and cryptographic event logs:

{log_data}

Provide a concise summary highlighting any unusual or critical events."

    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # Example log data (in a real scenario, this would come from an audit log system)
    example_log = """
    2023-10-27T10:00:01Z kms.googleapis.com/encrypt key_id=my-key project_id=my-project user=user1@example.com
    2023-10-27T10:00:05Z kms.googleapis.com/decrypt key_id=my-key project_id=my-project user=user2@example.com
    2023-10-27T10:01:00Z kms.googleapis.com/createKey key_id=new-key project_id=my-project user=admin@example.com
    2023-10-27T10:05:30Z kms.googleapis.com/encrypt key_id=my-key project_id=my-project user=user1@example.com
    2023-10-27T10:15:20Z kms.googleapis.com/decrypt key_id=my-key project_id=my-project user=user2@example.com
    2023-10-27T10:30:10Z kms.googleapis.com/asymmetricSign key_id=sign-key project_id=my-project user=user3@example.com
    2023-10-27T10:45:00Z kms.googleapis.com/destroyKeyVersion key_id=old-key-v1 project_id=my-project user=admin@example.com
    """

    try:
        summary = summarize_key_usage(example_log)
        print("Key Usage Summary:")
        print(summary)
    except Exception as e:
        print(f"Error summarizing key usage: {e}")
