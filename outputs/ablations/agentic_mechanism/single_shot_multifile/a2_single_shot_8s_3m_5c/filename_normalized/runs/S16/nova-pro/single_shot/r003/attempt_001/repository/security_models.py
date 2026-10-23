class SecretResponse:
    def __init__(self, raw_response):
        self.raw_response = raw_response

    def get_secret_string(self):
        return self.raw_response['SecretString']

    def get_version_id(self):
        return self.raw_response['VersionId']

    def get_arn(self):
        return self.raw_response['ARN']