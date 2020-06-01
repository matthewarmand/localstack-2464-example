import boto3


def get_localstack_s3_client(localstack_port):
    return boto3.client(
        "s3",
        endpoint_url=f"http://aws:{localstack_port}",
        aws_access_key_id="id",
        aws_secret_access_key="key",
    )
