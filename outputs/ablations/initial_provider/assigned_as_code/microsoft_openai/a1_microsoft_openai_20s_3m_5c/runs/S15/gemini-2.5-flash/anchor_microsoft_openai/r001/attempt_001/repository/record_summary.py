from openai import AzureOpenAI
import os

def record_summary(text_content):
    client = AzureOpenAI(
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"),  
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
        azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    )

    # Assuming a deployment name for the model, e.g., "text-davinci-003" or a chat model
    deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")

    try:
        # For older models like davinci, use client.completions.create
        # For chat models like gpt-35-turbo, use client.chat.completions.create
        # This example assumes a chat-based model.
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": f"Summarize the following text: {text_content}"}
            ]
        )
        return {'summary': response.choices[0].message.content.strip()}
    except Exception as e:
        print(f"Error summarizing text with Azure OpenAI: {e}")
        return {'summary': None, 'error': str(e)}
