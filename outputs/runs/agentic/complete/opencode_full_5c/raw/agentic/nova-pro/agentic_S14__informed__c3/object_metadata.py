import oss2


def object_metadata(bucket_name, object_name):
    auth = oss2.Auth(
        os.environ["ALIBABA_CLOUD_ACCESS_KEY_ID"],
        os.environ["ALIBABA_CLOUD_ACCESS_KEY_SECRET"],
    )
    bucket = oss2.Bucket(auth, "http://oss-cn-hangzhou.aliyuncs.com", bucket_name)
    metadata = bucket.head_object(object_name)
    print(f"Metadata for {object_name}: {metadata}")
    return metadata
