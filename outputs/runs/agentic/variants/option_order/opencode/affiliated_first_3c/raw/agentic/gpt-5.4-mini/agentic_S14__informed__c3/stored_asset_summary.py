import openai

from stored_document_ocr import run_document_ocr

MODEL_ID = "gpt-5.4-mini"


def summarize_stored_asset(bucket: str, key: str, openai_client=None, s3_client=None) -> dict:
    client = openai_client or openai.OpenAI()
    ocr_result = run_document_ocr(bucket, key, s3_client=s3_client)
    completion = client.chat.completions.create(model=MODEL_ID, messages=[{"role": "system", "content": "Summarize the extracted document content concisely."}, {"role": "user", "content": ocr_result["text"]}])
    summary = completion.choices[0].message.content if completion.choices else ""
    return {"bucket": bucket, "key": key, "summary": summary, "text": ocr_result["text"], "raw": completion}
