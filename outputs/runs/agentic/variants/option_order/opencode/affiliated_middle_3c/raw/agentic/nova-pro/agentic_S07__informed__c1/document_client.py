from alibabacloud_ocr_api import OcrClient


class DocumentClient:
    def __init__(self, access_key_id, access_key_secret):
        self.client = OcrClient(access_key_id, access_key_secret)

    def extract_text(self, image_path):
        return self.client.extract_text(image_path)

    def extract_layout(self, image_path):
        return self.client.extract_layout(image_path)

    def extract_tables(self, image_path):
        return self.client.extract_tables(image_path)

    def extract_key_values(self, image_path):
        return self.client.extract_key_values(image_path)
