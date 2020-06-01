import json
import pytest
import requests
import socket
import time

from django.conf import settings
from io import StringIO
from rest_framework import test

from example.clients import get_localstack_s3_client


@pytest.fixture
def api_client():
    return test.APIClient()


@pytest.fixture
def localstack():
    _wait_for_localstack()
    create_bucket_if_needed()


def create_bucket_if_needed():
    s3_client = get_localstack_s3_client(4566)
    if settings.AWS_STORAGE_BUCKET_NAME not in [
        o["Name"] for o in s3_client.list_buckets()["Buckets"]
    ]:
        s3_client.create_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
    return s3_client


def _wait_for_localstack():
    # Wait for Localstack container to be ready
    attempt_count = 0
    timeout = 10
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while attempt_count < timeout:
        try:
            result = s.connect_ex(("aws", 4566))
            if result == 0:
                s.shutdown(socket.SHUT_RDWR)
                s.close()
                return
        except socket.gaierror:
            pass
        attempt_count += 1
        if attempt_count != timeout:
            time.sleep(1)
    raise Exception("Unable to connect to AWS Localstack container")


@pytest.mark.parametrize("localstack_port", [(4566), (4572)])
def test_localstack_endpoint_with_post(api_client, localstack, localstack_port):
    response = api_client.post(
        "/example/",
        data=json.dumps(
            dict(filename="localstack-post.txt", localstack_port=localstack_port)
        ),
        content_type="application/json",
    )
    assert response.status_code == 201
    content = response.json()

    assert "upload_params" in content
    files = {"file": ("doesntmatter", StringIO("file contents"))}
    http_response = requests.post(
        content["upload_params"]["url"],
        data=content["upload_params"]["fields"],
        files=files,
    )
    # breakpoint()
    assert http_response.status_code == 204


def test_live_aws_with_post(api_client):
    response = api_client.post(
        "/example/",
        data=json.dumps(dict(filename="live-aws-post.txt")),
        content_type="application/json",
    )
    assert response.status_code == 201
    content = response.json()

    assert "upload_params" in content
    files = {"file": ("doesntmatter", StringIO("file contents"))}
    http_response = requests.post(
        content["upload_params"]["url"],
        data=content["upload_params"]["fields"],
        files=files,
    )
    # breakpoint()
    assert http_response.status_code == 204


@pytest.mark.parametrize("localstack_port", [(4566), (4572)])
def test_localstack_endpoint_with_put(api_client, localstack, localstack_port):
    response = api_client.post(
        "/example/",
        data=json.dumps(
            dict(filename="localstack-put.txt", localstack_port=localstack_port)
        ),
        content_type="application/json",
    )
    assert response.status_code == 201
    content = response.json()

    assert "upload_params" in content
    files = {"file": ("doesntmatter", StringIO("file contents"))}
    http_response = requests.put(
        content["upload_params"]["url"],
        data=content["upload_params"]["fields"],
        files=files,
    )
    # breakpoint()
    assert http_response.status_code == 200


def test_live_aws_with_put(api_client):
    response = api_client.post(
        "/example/",
        data=json.dumps(dict(filename="live-aws-put.txt")),
        content_type="application/json",
    )
    assert response.status_code == 201
    content = response.json()

    assert "upload_params" in content
    files = {"file": ("doesntmatter", StringIO("file contents"))}
    http_response = requests.put(
        content["upload_params"]["url"],
        data=content["upload_params"]["fields"],
        files=files,
    )
    # breakpoint()
    assert http_response.status_code == 200
