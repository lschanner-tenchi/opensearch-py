# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import sys

OPENSEARCH_SERVICE = "es"

PY3 = sys.version_info[0] == 3


class AWSV4SignerAsyncAuth:
    """
    AWS V4 Request Signer for Async Requests.
    """

    def __init__(self, credentials, region):  # type: ignore
        if not credentials:
            raise ValueError("Credentials cannot be empty")
        self.credentials = credentials

        if not region:
            raise ValueError("Region cannot be empty")
        self.region = region

    def __call__(self, method, url, query_string, body):  # type: ignore
        return self._sign_request(method, url, query_string, body)  # type: ignore

    def _sign_request(self, method, url, query_string, body):
        """
        This method helps in signing the request by injecting the required headers.
        :param prepared_request: unsigned headers
        :return: signed headers
        """
        from botocore.auth import SigV4Auth
        from botocore.awsrequest import AWSRequest

        # create an AWS request object and sign it using SigV4Auth
        print("".join([url, query_string]))
        aws_request = AWSRequest(
            method=method,
            url="".join([url, query_string]),
            data=body,
        )
        sig_v4_auth = SigV4Auth(self.credentials, OPENSEARCH_SERVICE, self.region)
        sig_v4_auth.add_auth(aws_request)

        # copy the headers from AWS request object into the prepared_request
        return dict(aws_request.headers.items())
