import os
import openai
from storage_client import get_s3_client
from storage_models import normalize_head_params

def summarize_stored_asset(bucket, key):
    """Generates a concise summary of the text content stored in an S3 object using GPT-4o.
    Downloads the object, extracts plain text, and calls OpenAI's chat completion API.
    """
    s3 = get_s3_client()
    # Download object to temporary file
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as tmp_file:
        s3.download_file(bucket, key, tmp_file.name)
        print(f'Downloaded {key} for summarization.')
        content = open(tmp_file.name, 'r', encoding='utf-8').read()
        os.unlink(tmp_file.name)
    # Generate summary via OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Summarize the following document in 3 sentences:\n\n{content}"}]
    )
    summary = response.choices[0].message.content.strip()
    print(f'Generated summary ({len(summary)} chars).')
    return summary
