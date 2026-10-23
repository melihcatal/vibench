import json

import boto3


def main(result_path: str):
    return json.dumps({"summary": boto3.session.Session().region_name, "source": result_path})
