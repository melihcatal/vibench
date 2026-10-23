class DynamoDBModel:
    def __init__(self, table_name):
        self.table_name = table_name


class S3Model:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
