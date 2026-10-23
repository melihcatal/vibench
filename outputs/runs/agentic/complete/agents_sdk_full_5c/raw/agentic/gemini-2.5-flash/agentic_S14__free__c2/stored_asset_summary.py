import boto3
import json
from storage_client import get_bedrock_runtime_client

def summarize_text_with_bedrock(text: str, model_id: str = "anthropic.claude-v2") -> str:
    """
    Summarizes content extracted from a stored asset using an AWS Bedrock generative AI model.
    Requires a model that supports text generation (e.g., Anthropic Claude, AI21 Labs Jurassic).
    """
    bedrock_runtime = get_bedrock_runtime_client()
    
    prompt = f"""Human: Summarize the following text:

<text>
{text}
</text>

Assistant:"""

    # The request body depends on the model you are using.
    # This example is for Anthropic Claude models.
    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": 500,
        "temperature": 0.5,
        "top_p": 0.9,
    })

    try:
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            contentType='application/json',
            accept='application/json',
            body=body
        )
        
        response_body = json.loads(response['body'].read())
        # The output key also depends on the model.
        # For Claude, it's 'completion'.
        summary = response_body.get('completion', '')
        return summary.strip()
    except bedrock_runtime.exceptions.ClientError as e:
        print(f"Error invoking Bedrock model for summarization: {e}")
        raise

if __name__ == '__main__':
    # Example usage:
    # long_text = """
    # Amazon Elastic Compute Cloud (Amazon EC2) is a web service that provides resizable compute capacity in the cloud.
    # It is designed to make web-scale cloud computing easier for developers. Amazon EC2's simple web service interface
    # allows you to obtain and configure capacity with minimal friction. It provides you with complete control of your
    # computing resources and lets you run on Amazon's proven computing environment. The service virtually eliminates
    # your need to invest in hardware up front, so you can develop and deploy applications faster.
    # You can use Amazon EC2 to launch as many or as few virtual servers as you need, configure security and networking,
    # and manage storage. Amazon EC2 enables you to scale up or down to handle changes in requirements or spikes in popularity,
    # reducing your need to forecast traffic.
    # """
    # try:
    #     # Make sure the specified model ID is enabled in your AWS Bedrock account and region
    #     summary = summarize_text_with_bedrock(long_text, model_id="anthropic.claude-v2") # or "amazon.titan-text-express-v1"
    #     print(f"Original Text:\n{long_text}\n")
    #     print(f"Summary:\n{summary}")
    # except Exception as e:
    #     print(f"Summarization failed: {e}")
    pass
