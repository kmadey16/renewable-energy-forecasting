import boto3
import os
from pathlib import Path
from dotenv import load_dotenv

# Load secrets from .env
load_dotenv()

aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_DEFAULT_REGION")

# Define s3 settings
bucket_name = "renewable-energy-forecasting"
s3_prefix = "raw/"  # Folder in your S3 bucket
local_folder = Path("data/raw/")

# initialize s3
s3 = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region
)

# upload csvs
def upload_files():
    files = list(local_folder.glob("*.csv"))
    if not files:
        print("No CSV files found in data/raw/")
        return
#loop through and upload
    for file in files:
        s3_key = f"{s3_prefix}{file.name}"
        print(f"Uploading {file.name} → s3://{bucket_name}/{s3_key}")
        s3.upload_file(str(file), bucket_name, s3_key)

    print("Upload complete!")
# run if script is executed
if __name__ == "__main__":
    upload_files()
