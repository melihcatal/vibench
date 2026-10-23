import oss2


def presigned_download(bucket_name, object_name):
    auth = oss2.Auth(
        os.environ["ALIBABA_CLOUD_ACCESS_KEY_ID"],
        os.environ["ALIBABA_CLOUD_ACCESS_KEY_SECRET"],
    )
    bucket = oss2.Bucket(auth, "http://oss-cn-hangzhou.aliyuncs.com", bucket_name)
    url = bucket.sign_url("GET", object_name, 3600)
    print(f"Presigned URL for {object_name}: {url}")
    return url
