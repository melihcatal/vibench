import os
from openai import AzureOpenAI

def answer_with_context(question: str, context: str) -> str:
    """
    Calls Azure OpenAI to answer a question using provided context.
    """
    client = AzureOpenAI(
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        api_version="2024-02-01", # Or your preferred API version
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT")
    )

    # Replace with your actual deployment name
    deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-35-turbo") 

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context."},
            {"role": "user", "content": f"Context: {context}\nQuestion: {question}"}
        ],
        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].message.content
