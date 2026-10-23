import json
import os
from typing import Dict, Any
from database_client import get_bedrock_client
from database_models import RecordSummaryRequest, RecordSummaryResponse


def record_summary(request: RecordSummaryRequest) -> RecordSummaryResponse:
    """
    Summarize retrieved document records using Amazon Bedrock.
    """
    bedrock = get_bedrock_client()

    try:
        document_text = ""
        for field in request.fields_to_summarize:
            if field in request.document:
                value = request.document[field]
                if isinstance(value, str):
                    document_text += f"{field}: {value}\n"
                elif isinstance(value, (dict, list)):
                    document_text += f"{field}: {json.dumps(value)}\n"
                else:
                    document_text += f"{field}: {str(value)}\n"

        prompt = f"""Please provide a concise summary of the following document data. 
        Focus on the key information and keep the summary under {request.max_length} characters.
        
        Document data:
        {document_text}
        
        Summary:"""

        model_id = "anthropic.claude-3-haiku-20240307-v1:0"

        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 500,
                "messages": [{"role": "user", "content": prompt}],
            }
        )

        response = bedrock.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=body,
        )

        response_body = json.loads(response["body"].read())
        summary = response_body["content"][0]["text"].strip()

        if len(summary) > request.max_length:
            summary = summary[: request.max_length].rsplit(" ", 1)[0] + "..."

        return RecordSummaryResponse(
            success=True,
            summary=summary,
            message="Document summarized successfully using Amazon Bedrock",
        )
    except Exception as e:
        return RecordSummaryResponse(
            success=False,
            summary="",
            error_message=str(e),
            message="Failed to summarize document",
        )
