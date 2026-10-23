import os
import boto3
import json
from storage_client import get_bedrock_runtime_client
from storage_models import SummaryResult

def summarize_text_with_bedrock(text: str, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0") -> SummaryResult | None:
    """
    Summarizes the given text using a specified model via Amazon Bedrock Runtime.
    :param text: The text to summarize.
    :param model_id: The ID of the model to use for summarization (e.g., "anthropic.claude-3-sonnet-20240229-v1:0", "amazon.titan-text-express-v1").
    :return: SummaryResult object or None if an error occurs.
    """
    bedrock_runtime = get_bedrock_runtime_client()

    # The payload structure depends on the model provider.
    # This example uses the Anthropic Claude format.
    # For Titan, it would be different (e.g., {'inputText': text, 'textGenerationConfig': {'maxTokenCount': 500}})
    
    if model_id.startswith("anthropic."):
        prompt = f"Human: Summarize the following document concisely:\n\n<document>\n{text}\n</document>\n\nAssistant:"
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 500,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })
        
    elif model_id.startswith("amazon.titan-text"):
        prompt = f"Summarize the following text:\n\n{text}"
        body = json.dumps({"inputText": prompt, "textGenerationConfig": {"maxTokenCount": 500, "temperature": 0.7}})
    else:
        print(f"Unsupported model ID for summarization: {model_id}")
        return None

    try:
        response = bedrock_runtime.invoke_model(
            body=body,
            modelId=model_id,
            accept='application/json',
            contentType='application/json'
        )
        
        response_body = json.loads(response.get('body').read())

        summary_text = ""
        if model_id.startswith("anthropic."):
            summary_text = response_body['content'][0]['text']
        elif model_id.startswith("amazon.titan-text"):
            summary_text = response_body['results'][0]['outputText']
        
        return SummaryResult(
            summary_text=summary_text,
            model_id=model_id
        )

    except Exception as e:
        print(f"Error summarizing text with Bedrock model {model_id}: {e}")
        return None

if __name__ == '__main__':
    # Example usage
    sample_long_text = (
        "The Amazon rainforest is the largest rainforest in the world, covering much of "
        "northwestern South America. It's known for its biodiversity, with millions of "
        "species of insects, plants, birds, and other forms of life. The forest is home "
        "to over 30 million people, including hundreds of indigenous groups. Deforestation "
        "is a major concern, threatening the unique ecosystem and contributing to climate change. "
        "Efforts are underway to conserve the Amazon and promote sustainable practices." * 5
    )
    
    print("Summarizing with Anthropic Claude on Bedrock...")
    claude_summary = summarize_text_with_bedrock(sample_long_text, model_id="anthropic.claude-3-sonnet-20240229-v1:0")
    if claude_summary:
        print(f"Model: {claude_summary.model_id}")
        print(f"Summary: {claude_summary.summary_text}")
    else:
        print("Claude summarization failed.")

    print("\nSummarizing with Amazon Titan on Bedrock (if available and uncommented)...")
    # titan_summary = summarize_text_with_bedrock(sample_long_text, model_id="amazon.titan-text-express-v1")
    # if titan_summary:
    #     print(f"Model: {titan_summary.model_id}")
    #     print(f"Summary: {titan_summary.summary_text}")
    # else:
    #     print("Titan summarization failed.")
