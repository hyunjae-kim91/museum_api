import os
import boto3
from dotenv import load_dotenv
load_dotenv()

class S3Connector:
    """S3에서 파일 read와 put을 수행합니다."""
    def __init__(self, **kwargs):
        access_key_id = kwargs.get('access_key_id')
        secret_key = kwargs.get('secret_key')
        bucket = kwargs.get('bucket')
        s3 = boto3.resource(
            's3', 
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_key
        )
        self.bucket = s3.Bucket(bucket)
    
    def put_file(self, file_path: str, file_name: str, s3_path: str, s3_file_name: str) -> None:
        """파일 put 수행"""
        self.bucket.upload_file(f"{file_path}/{file_name}", f"{s3_path}/{s3_file_name}")

    def download_file(self, file_path: str, file_name: str, s3_path: str) -> None:
        self.bucket.download_file(f"{s3_path}/{file_name}", f"{file_path}/{file_name}")

        
s3_conf = {
    "access_key_id": os.environ.get("s3_access_key_id"),
    "secret_key": os.environ.get("s3_secret_key"),
    "bucket": os.environ.get("bucket")
}

s3Connector = S3Connector(**s3_conf)
