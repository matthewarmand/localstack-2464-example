# localstack-2464-example

Example code to illustrate issue described in [localstack/localstack#2464](https://github.com/localstack/localstack/issues/2464)

I've noticed some odd dissonance in behavior regarding S3 Presigned URLs. I'm using a pattern
consistent with [`boto3`'s docs](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html).
Here's a summary of the behavior I'm seeing:

- Using `boto3`'s [`generate_presigned_post`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.generate_presigned_post),
it is possible to successfully `POST` a file to live AWS S3 as well as Localstack via the deprecated
service-specific port (`4572`).

- The above operation fails with a `404` for Localstack's edge port (`4566`).

- Additionally (and as a side note) the above operation succeeds using a `PUT` on both Localstack
ports (`4566` and `4572`), but fails schema validation on live AWS S3 with a `400`.

Ultimately I'm less concerned about the `PUT`; `generate_presigned_post` should only really be
supported on `POST` anyway. The behavior _should_ however be consistent across both relevant
Localstack ports and live AWS.

# Setup and running tests

1. Copy .env.tmpl and supply your values. `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` are both
only used for connecting to AWS. They are ignored/overridden when talking to Localstack (This is
a convenience to avoid leaking actual creds in localstack logs). Supply those two as well as a
bucket to which you have access to test the live upload.

    ```
    cp .env.tmpl .env
    ```

1. Build container

    ```
    docker-compose build
    ```

1. Run tests

    ```
    docker-compose run web pytest
    ```

# Other helpful commands

1. Run a single test

    ```
    docker-compose run web pytest -k <test_case_name>
    ```

1. Stand up the API for manual interaction (with `curl` for example)

    ```
    docker-compose up
    ```
