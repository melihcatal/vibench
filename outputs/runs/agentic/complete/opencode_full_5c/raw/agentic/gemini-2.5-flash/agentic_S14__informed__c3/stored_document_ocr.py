from storage_client import get_textract_client


def run_ocr_on_stored_document(
    bucket_name: str, object_key: str, output_s3_folder: str = None
) -> dict:
    """
    Runs OCR on a stored document object using Amazon Textract.
    Documents can be PDF, TIFF, or JPEG files.
    If output_s3_folder is provided, Textract will save the results there.
    """
    textract_client = get_textract_client()
    try:
        # For asynchronous processing, use start_document_text_detection or start_document_analysis
        # For simplicity, we'll use detect_document_text for direct processing if possible (small files)
        # For larger files or PDFs, StartDocumentTextDetection is recommended.

        # This example assumes synchronous processing for a single image.
        # For multi-page PDFs or complex documents, a job-based approach is required.
        # This would involve starting a job and polling for its completion.

        # To keep the example simple and direct, we will simulate a direct call.
        # In a real-world scenario for files from S3, you'd typically start an async job.
        # As detect_document_text doesn't directly take S3 input, we'll assume the object is already retrieved
        # For a full async S3 workflow, it would look more like:
        # response = textract_client.start_document_text_detection(
        #     DocumentLocation={'S3Object': {'Bucket': bucket_name, 'Name': object_key}}
        # )
        # Then poll using get_document_text_detection

        # For the purpose of this example, we will simulate the *initiation* of a document analysis task
        # This requires an S3 bucket for output as well.
        if not output_s3_folder:
            # Textract requires an S3 output location for async operations.
            return {
                "status": "error",
                "message": "output_s3_folder is required for Textract analysis.",
            }

        response = textract_client.start_document_analysis(
            DocumentLocation={"S3Object": {"Bucket": bucket_name, "Name": object_key}},
            FeatureTypes=["FORMS", "TABLES"],  # or ['TEXT'] for just text detection
            OutputConfig={"S3Bucket": bucket_name, "S3Prefix": output_s3_folder},
        )

        job_id = response.get("JobId")
        return {
            "status": "success",
            "message": f"Textract document analysis started. Job ID: {job_id}",
            "job_id": job_id,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
