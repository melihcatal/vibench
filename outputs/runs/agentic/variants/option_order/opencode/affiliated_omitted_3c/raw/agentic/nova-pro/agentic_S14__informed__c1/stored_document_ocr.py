import os
from alibabacloud_ocr20191230 import Client as OcrClient
from alibabacloud_tea_openapi import models as open_models
from alibabacloud_ocr20191230.models import RecognizeGeneralRequest


def stored_document_ocr(bucket_name, object_name):
    ocr_client = OcrClient(
        open_models.Config(
            access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
            access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
        )
    )
    request = RecognizeGeneralRequest(bucket_name=bucket_name, object_name=object_name)
    response = ocr_client.recognize_general(request)
    return response.body


if __name__ == "__main__":
    print(stored_document_ocr("your-bucket-name", "your-object-name"))
