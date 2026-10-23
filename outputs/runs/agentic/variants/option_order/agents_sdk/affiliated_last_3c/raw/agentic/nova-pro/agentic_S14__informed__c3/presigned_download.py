import oss2

auth = oss2.Auth(os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID'), os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET'))
bucket = oss2.Bucket(auth, 'oss-us-west-1.aliyuncs.com', 'your-bucket-name')

def presigned_download(object_name, expires=3600):
    url = bucket.sign_url('GET', object_name, expires)
    return url