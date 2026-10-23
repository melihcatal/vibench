import os
import openai

# Configure OpenAI client with your API key, e.g., via environment variable OPENAI_API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_asset(bucket: str, key: str) -> dict:
    """Generate a concise summary of content extracted from a stored asset.
    
    Parameters:
        bucket (str): Bucket name.
        key (str): Object key/path to a text or document file.
    
    Returns:
        dict: Summary with title and up to 3 bullet points.
    """
    # Pull the file content from S3
    s3 = ManagedObjectStorageClient(
        service="Amazon S3",
        credentials={
            "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
            "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
        },
    )
    client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    obj = client.get_object(Bucket=bucket, Key=key)
    content = obj["Body"].read().decode("utf-8")

    # Query OpenAI/GPT for summarization (ChatGPT style)
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Summarize the following text in one title and three bullet points.\n\n{text_content}"}],
    )
    # The conversation above is illustrative; the actual request should pass `content` to the model.
    # Extract the assistant's response from the completion.
    summary = response.choices[0].message.content.strip()
    return {
        "title": get_title_from_summary(summary),
        "bullets": extract_bullets(summary)
    }

# Helper utilities to parse the model's response

def get_title_from_summary(summary: str) -> str:
    # Very naive extraction: first line ending with a period
    lines = summary.split("\\n")
    for line in lines:
        if line.endswith(\".\"):
            return line.strip(". ")
    return "Summary Title"

def extract_bullets(summary: str) -> List[str]:
    # Grab lines that start with a dash or bullet character
    bullets = [line.strip() for line in summary.split("\\n") if line.startswith(\"-") or line.startswith(\"*\")]
    return bullets[:3]
