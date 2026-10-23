"""
[LATER-STEP] compliance_note_translate.py
Translate encryption or compliance notes for reviewers using AWS Bedrock.
Provider: AWS Bedrock (bedrock.amazonaws.com)
Uses anthropic.claude-3-sonnet-20240229-v1:0 model for translation tasks.
"""

import json
import sys
from typing import Optional, Dict, Any

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from security_client import KMSClientConfig

AWS_BEDROCK_ENDPOINT = "bedrock.amazonaws.com"
AWS_BEDROCK_RUNTIME_SERVICE = "bedrock-runtime"

CLAUDE_SONNET_MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"
CLAUDE_HAIKU_MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"
CLAUDE_OPUS_MODEL_ID = "anthropic.claude-3-opus-20240229-v1:0"


def create_bedrock_runtime_client(
    config: Optional[KMSClientConfig] = None,
):
    """Create an AWS Bedrock Runtime client for inference operations."""
    if config is None:
        config = KMSClientConfig()

    client_config = Config(retries={"max_attempts": 3})
    session_kwargs = {"region_name": config.region}
    if config.aws_access_key_id and config.aws_secret_access_key:
        session_kwargs["aws_access_key_id"] = config.aws_access_key_id
        session_kwargs["aws_secret_access_key"] = config.aws_secret_access_key
    if config.aws_session_token:
        session_kwargs["aws_session_token"] = config.aws_session_token

    session = boto3.Session(**session_kwargs)
    return session.client(AWS_BEDROCK_RUNTIME_SERVICE, config=client_config)


def translate_compliance_note(
    compliance_note: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
    model_id: str = CLAUDE_SONNET_MODEL_ID,
    config: Optional[KMSClientConfig] = None,
) -> Dict[str, Any]:
    """
    Translate an encryption or compliance note for international reviewers
    using Anthropic Claude on AWS Bedrock.
    Model: anthropic.claude-3-sonnet-20240229-v1:0
    """
    bedrock_client = create_bedrock_runtime_client(config)

    source_lang_instruction = ""
    if source_language:
        source_lang_instruction = f" from {source_language}"

    prompt = f"""You are a professional translator specializing in cryptography and compliance documentation.

Please translate the following encryption/compliance note{source_lang_instruction} to {target_language}.
Preserve all technical terms, key identifiers, and compliance references accurately.
Maintain the formal tone appropriate for audit documentation.

Compliance Note:
{compliance_note}

Translation:"""

    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2048,
            "temperature": 0.1,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        }
    )

    try:
        response = bedrock_client.invoke_model(
            modelId=model_id,
            body=body,
            accept="application/json",
            contentType="application/json",
        )

        response_body = json.loads(response.get("body").read())
        content_blocks = response_body.get("content", [])
        translated_text = ""

        for block in content_blocks:
            if block.get("type") == "text":
                translated_text += block.get("text", "")

        return {
            "success": True,
            "original_text": compliance_note,
            "translated_text": translated_text.strip(),
            "source_language": source_language or "auto-detected",
            "target_language": target_language,
            "model_id": model_id,
            "provider": "aws-bedrock",
            "endpoint": AWS_BEDROCK_ENDPOINT,
        }

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "Unknown")
        error_message = e.response.get("Error", {}).get("Message", str(e))
        return {
            "success": False,
            "error": f"Bedrock error: {error_code} - {error_message}",
            "provider": "aws-bedrock",
            "endpoint": AWS_BEDROCK_ENDPOINT,
        }


def translate_compliance_notes_batch(
    compliance_notes: list,
    target_language: str = "en",
    model_id: str = CLAUDE_SONNET_MODEL_ID,
    config: Optional[KMSClientConfig] = None,
) -> Dict[str, Any]:
    """
    Translate multiple compliance notes sequentially using AWS Bedrock Claude.
    """
    translations = []
    failed_notes = []

    for idx, note in enumerate(compliance_notes):
        result = translate_compliance_note(
            compliance_note=note,
            target_language=target_language,
            model_id=model_id,
            config=config,
        )

        if result.get("success"):
            translations.append(
                {
                    "index": idx,
                    "original_preview": note[:80] + "..." if len(note) > 80 else note,
                    "translated_text": result["translated_text"],
                    "target_language": target_language,
                }
            )
        else:
            failed_notes.append({"index": idx, "error": result.get("error")})

    return {
        "success": len(failed_notes) == 0,
        "total_notes": len(compliance_notes),
        "successful_translations": len(translations),
        "failed_notes": len(failed_notes),
        "translations": translations,
        "failures": failed_notes,
        "model_id": model_id,
        "provider": "aws-bedrock",
        "endpoint": AWS_BEDROCK_ENDPOINT,
    }


def summarize_compliance_note(
    compliance_note: str,
    model_id: str = CLAUDE_SONNET_MODEL_ID,
    config: Optional[KMSClientConfig] = None,
) -> Dict[str, Any]:
    """
    Summarize a complex compliance note for executive review using Claude.
    """
    bedrock_client = create_bedrock_runtime_client(config)

    prompt = f"""You are a compliance documentation specialist.

Please provide a concise executive summary of the following encryption compliance note.
Focus on key actions, compliance requirements, and any critical dates or deadlines.
Keep the summary to 3-5 sentences.

Compliance Note:
{compliance_note}

Executive Summary:"""

    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 512,
            "temperature": 0.1,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        }
    )

    try:
        response = bedrock_client.invoke_model(
            modelId=model_id,
            body=body,
            accept="application/json",
            contentType="application/json",
        )

        response_body = json.loads(response.get("body").read())
        content_blocks = response_body.get("content", [])
        summary_text = ""

        for block in content_blocks:
            if block.get("type") == "text":
                summary_text += block.get("text", "")

        return {
            "success": True,
            "original_text": compliance_note,
            "executive_summary": summary_text.strip(),
            "model_id": model_id,
            "provider": "aws-bedrock",
            "endpoint": AWS_BEDROCK_ENDPOINT,
        }

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "Unknown")
        error_message = e.response.get("Error", {}).get("Message", str(e))
        return {
            "success": False,
            "error": f"Bedrock error: {error_code} - {error_message}",
            "provider": "aws-bedrock",
        }


def compliance_note_translate_to_json(
    compliance_note: str,
    target_language: str = "en",
    config: Optional[KMSClientConfig] = None,
) -> str:
    """Translate a compliance note and return as JSON string."""
    result = translate_compliance_note(
        compliance_note=compliance_note,
        target_language=target_language,
        config=config,
    )
    return json.dumps(result, indent=2, default=str)


if __name__ == "__main__":
    sample_note = (
        "Encryption key rotation completed for production environment. "
        "All AES-256-GCM encrypted data has been re-encrypted with the new "
        "CMK (arn:aws:kms:us-east-1:123456789012:key/abcd1234-a123-456a-a12b-a123b1234cde). "
        "Compliance validation per SOC2 Type II and ISO 27001 requirements confirmed."
    )

    result = translate_compliance_note(
        compliance_note=sample_note,
        target_language="es",
        source_language="en",
    )

    print(json.dumps(result, indent=2, default=str))
