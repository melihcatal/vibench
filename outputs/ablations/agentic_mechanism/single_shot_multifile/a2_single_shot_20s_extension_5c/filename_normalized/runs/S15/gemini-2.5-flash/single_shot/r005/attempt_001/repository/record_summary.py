import os
import json
from database_client import get_bedrock_client
from database_models import Document

CLAUDE_MODEL_ID = os.environ.get('BEDROCK_CLAUDE_MODEL_ID', 'anthropic.claude-3-sonnet-20240229-v1:0')

def summarize_document_content(document: Document) -> str:
    bedrock_runtime = get_bedrock_client()

    prompt = f"""Human: Summarize the following document content concisely:

<document_content>
{document.content}
</document_content>

Assistant:"""

    body = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 200,
        "temperature": 0.5
    })

    response = bedrock_runtime.invoke_model(
        body=body,
        contentType='application/json',
        accept='application/json',
        modelId=CLAUDE_MODEL_ID
    )

    response_body = json.loads(response['body'].read())
    summary = response_body['content'][0]['text']
    return summary
