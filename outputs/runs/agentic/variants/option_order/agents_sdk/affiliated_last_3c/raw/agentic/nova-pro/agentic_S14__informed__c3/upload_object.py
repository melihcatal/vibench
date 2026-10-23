import oss2

auth = oss2.Auth(os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID'), os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET'))
bucket = oss2.Bucket(auth, 'oss-us-west-1.aliyuncs.com', 'your-bucket-name')

def upload_object(file_path, object_name):
    with open(file_path, 'rb') as file_data:
        bucket.put_object(object_name, file_data))