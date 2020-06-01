import boto3
import os

from django.conf import settings
from rest_framework import serializers

from example.clients import get_localstack_s3_client


class ExampleSerializer(serializers.Serializer):
    filename = serializers.CharField()
    localstack_port = serializers.IntegerField(required=False, allow_null=True)
    upload_params = serializers.DictField(read_only=True)

    def create(self, validated_data):
        filename = validated_data["filename"]
        localstack_port = validated_data.get("localstack_port", None)
        return dict(
            filename=filename,
            upload_params=self._create_presigned_post(
                filename, localstack_port=localstack_port
            ),
        )

    def _create_presigned_post(self, filename, localstack_port=None):
        s3_client = (
            get_localstack_s3_client(localstack_port)
            if localstack_port is not None
            else boto3.client("s3")
        )
        key = os.path.join("localstack-2464-example-testing/", filename)
        response = s3_client.generate_presigned_post(
            settings.AWS_STORAGE_BUCKET_NAME, key,
        )
        # The response contains the presigned URL and required fields
        return response
