import os
try:
    import boto3

    from mydemo.settings import S3_ACCESS_KEY, S3_ACCESS_KEY,S3_SESSION_TOKEN, S3_BUCKET
    client = boto3.client(
        's3',
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_ACCESS_KEY,
        aws_session_token=S3_SESSION_TOKEN
        )
except ImportError as e:
    print(str(e))
    print("pip install boto3, for support aws-s3")


class S3Client(object):
    def __init__(self) -> None:
        self.bucket = S3_BUCKET
        self.client = client
    
    def upload_file(self, path, object_name=None):
        if object_name is None:
            object_name = os.path.join("/", os.path.basename(object_name))
        try:
            self.client.upload_file(path, self.bucket, object_name)
            return object_name
        except Exception as e:
            print(e)

    
    def download_file(self, object_name, path):
        with open(path, 'wb') as f:
            self.client.download_fileobj(self.bucket, object_name, f)
        return path

