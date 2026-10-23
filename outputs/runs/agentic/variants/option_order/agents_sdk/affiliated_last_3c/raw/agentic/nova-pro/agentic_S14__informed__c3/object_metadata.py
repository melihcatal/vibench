import oss2

auth = oss2.Auth(os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID'), os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET'))
bucket = oss2.Bucket(auth, 'oss-us-west-1.aliyuncs.com', 'your-bucket-name')

def object_metadata(object_name):
    metadata = bucket.head_object(object_name)
    return metadata