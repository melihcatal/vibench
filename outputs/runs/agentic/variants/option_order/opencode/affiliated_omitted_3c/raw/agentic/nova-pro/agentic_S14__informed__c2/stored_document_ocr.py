import os
from alibabacloud_ocr20191230.client import Client as OcrClient
from alibabacloud_tea_openapi import models as open_models
from alibabacloud_ocr20191230 import models as ocr_models


def ocr_document(bucket_name, file_name):
    config = open_models.Config(
        access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    )
    client = OcrClient(config)
    request = ocr_models.RecognizeGeneralTableRequest(
        document_url=f"http://oss.aliyuncs.com/{bucket_name}/{file_name}"
    )
    response = client.recognize_general_table(request)
    return response.to_map()
