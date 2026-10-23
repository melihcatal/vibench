import oss2

def create_client(bucket_name):
    auth = oss2.Auth(os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID'), os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET'))
    bucket = oss2.Bucket(auth, 'oss-us-west-1.aliyuncs.com', bucket_name)
    return bucket