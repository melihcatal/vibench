import oss2


def get_client():
    auth = oss2.Auth(
        os.environ["ALIBABA_CLOUD_ACCESS_KEY_ID"],
        os.environ["ALIBABA_CLOUD_ACCESS_KEY_SECRET"],
    )
    bucket = oss2.Bucket(
        auth,
        "http://oss-cn-hangzhou.aliyuncs.com",
        os.environ["ALIBABA_CLOUD_BUCKET_NAME"],
    )
    return bucket
