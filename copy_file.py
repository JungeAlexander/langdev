import boto3

s3_client = boto3.client("s3")
fname = "requirements.txt"
s3_client.upload_file(fname, "rbpitv-kbase-ajs-aws", fname)
