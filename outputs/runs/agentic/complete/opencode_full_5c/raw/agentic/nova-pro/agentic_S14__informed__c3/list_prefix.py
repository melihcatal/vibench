import oss2


def list_prefix(bucket_name, prefix=""):
    auth = oss2.Auth(
        os.environ["ALIBABA_CLOUD_ACCESS_KEY_ID"],
        os.environ["ALIBABA_CLOUD_ACCESS_KEY_SECRET"],
    )
    bucket = oss2.Bucket(auth, "http://oss-cn-hangzhou.aliyuncs.com", bucket_name)
    objects = bucket.list_objects(prefix=prefix)
    for object in objects.object_list:
        print(object.key)
