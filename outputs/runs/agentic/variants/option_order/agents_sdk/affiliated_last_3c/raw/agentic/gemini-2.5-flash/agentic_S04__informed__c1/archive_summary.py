import os
from openai import AzureOpenAI

def summarize_transcript(transcript_text: str) -> str:
    # Azure OpenAI credentials
    # Set these environment variables: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT_NAME
    azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-15-preview") # Default to a recent version
    deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME") # e.g., gpt-35-turbo, gpt-4

    if not azure_endpoint or not api_key or not deployment_name:
        raise ValueError("AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, and AZURE_OPENAI_DEPLOYMENT_NAME environment variables must be set for Azure OpenAI.")

    try:
        client = AzureOpenAI(
            azure_endpoint=azure_endpoint,
            api_key=api_key,
            api_version=api_version
        )

        response = client.chat.completions.create(
            model=deployment_name, # This is the deployment name you chose for your model
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts concisely."}, 
                {"role": "user", "content": f"Please summarize the following transcript:\n\n{transcript_text}"}
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        if response.choices and response.choices[0].message and response.choices[0].message.content:
            return response.choices[0].message.content.strip()
        else:
            return "Summary generation failed: No content in response."

    except Exception as e:
        print(f"Error summarizing transcript with Azure OpenAI: {e}")
        return f"Summary generation failed due to an error: {e}"

if __name__ == '__main__':
    # Example usage
    # sample_transcript = (
    #     "Good morning everyone. Today we will discuss the Q3 financial results. "
    #     "Sales increased by 15% compared to the previous quarter, largely due to "
    #     "successful marketing campaigns in Europe. However, profit margins were slightly "
    #     "down due to increased operational costs. We need to review our spending "
    #     "in the next quarter. The team also presented new product development plans "
    #     "for the next year, focusing on AI integration. Overall, a positive outlook "
    #     "with areas for improvement."
    # )
    # summary = summarize_transcript(sample_transcript)
    # print("\n--- Original Transcript ---")
    # print(sample_transcript)
    # print("\n--- Generated Summary ---")
    # print(summary)
    pass
