import os
import mimetypes
import boto3
from google.cloud import storage
from dotenv import load_dotenv


load_dotenv()

class S3Uploader:

    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_ID'),
            aws_secret_access_key=os.getenv('AWS_ACCESS_PWD')
        )

    def upload(self, file_path: str, bucket_name: str):

        file_key = os.path.relpath(file_path)
        try:
            self.s3_client.upload_file(file_path, bucket_name, file_key)
            print(f"Successfully uploaded {file_path} to S3 bucket '{bucket_name}'")
        except Exception as e:
            print(f"Failed to upload {file_path} to S3: {e}")

class GCSUploader:
    
    def __init__(self):
        
        self.gcs_client = storage.Client()

    def upload(self, file_path: str, bucket_name: str):
        bucket = self.gcs_client.bucket(bucket_name)
        blob = bucket.blob(os.path.relpath(file_path))
        try:
            blob.upload_from_filename(file_path)
            print(f"Successfully uploaded {file_path} to GCS bucket '{bucket_name}'")
        except Exception as e:
            print(f"Failed to upload {file_path} to GCS: {e}")

def transfer_files(directory_path: str, s3_bucket_name: str, gcs_bucket_name: str, s3_file_extensions: list, gcs_file_extensions: list):
    s3_uploader = S3Uploader()
    gcs_uploader = GCSUploader()

    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_extension = os.path.splitext(file_name)[1].lower()

            if file_extension in s3_file_extensions:
                s3_uploader.upload(file_path, s3_bucket_name)
            elif file_extension in gcs_file_extensions:
                gcs_uploader.upload(file_path, gcs_bucket_name)
            else:
                print(f"Skipping {file_path} - Unsupported file type")

def main():
    directory_path = os.getenv('DIRECTORY_PATH', '/path/to/your/directory')
    s3_bucket_name = os.getenv('S3_BUCKET_NAME', 'your-s3-bucket-name')
    gcs_bucket_name = os.getenv('GCS_BUCKET_NAME', 'your-gcs-bucket-name')
    s3_file_extensions = os.getenv('S3_FILE_EXTENSIONS', '.jpg,.png,.svg,.webp,.mp3,.mp4,.mpeg4,.wmv,.3gp,.webm').split(',')
    gcs_file_extensions = os.getenv('GCS_FILE_EXTENSIONS', '.doc,.docx,.csv,.pdf').split(',')
    s3_file_extensions = [ext.lower() for ext in s3_file_extensions]
    gcs_file_extensions = [ext.lower() for ext in gcs_file_extensions]
    transfer_files(directory_path, s3_bucket_name, gcs_bucket_name, s3_file_extensions, gcs_file_extensions)

if __name__ == '__main__':
    main()

