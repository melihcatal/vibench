import oss2


def upload_object(bucket_name, object_name, file_path):
    auth = oss2.Auth(
        os.environ["ALIBABA_CLOUD_ACCESS_KEY_ID"],
        os.environ["ALIBABA_CLOUD_ACCESS_KEY_SECRET"],
    )
    bucket = oss2.Bucket(auth, "http://oss-cn-hangzhou.aliyuncs.com", bucket_name)
    bucket.put_object_from_file(object_name, file_path)
    print(f"Uploaded {file_path} to {bucket_name}/{object_name}")
