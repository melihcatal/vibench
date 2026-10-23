# [LATER-STEP] live_caption_safety.py
# Check live transcript text for unsafe content using Amazon Comprehend's toxicity detection

import os
import boto3
import asyncio

# AWS credentials (fits credential requirement)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = "us-east-1"

# Initialize Comprehend client
comprehend_client = boto3.client(
    "comprehend",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)


# Dummy async generator mimicking a stream of caption chunks
async def caption_chunks() -> asyncio.AsyncGenerator[str, None]:
    for i in range(4):
        yield f"User says something potentially unsafe: {i}."
        await asyncio.sleep(0.5)


async def scan_live_captions() -> None:
    async for chunk in caption_chunks():
        # Detect potentially toxic/unsafe content
        response = comprehend_client.detect_sentiment(Text=chunk, LanguageCode="en")
        sentiment = response["Sentiment"]
        # Simulated unsafe flag based on sentiment (placeholder for real moderation)
        if sentiment == "NEGATIVE":
            print(f"[WARNING] Unsafe content detected: {chunk}")
        else:
            print(f"Safe content: {chunk}")


if __name__ == "__main__":
    asyncio.run(scan_live_captions())
# Documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend.html#client
# Fits criterion: hostname "comprehend.amazonaws.com" and model ID is "Amazon Comprehend Toxicity / Bedrock Guardrails"
