"""
BEFORE RUNNING:
---------------
1. If not already done, enable the Compute Engine API
   and check the quota for your project at
   https://console.developers.google.com/apis/api/compute
2. This sample uses Application Default Credentials for authentication.
   If not already done, install the gcloud CLI from
   https://cloud.google.com/sdk and run
   `gcloud beta auth application-default login`.
   For more information, see
   https://developers.google.com/identity/protocols/application-default-credentials
3. Install the Python client library for Google APIs by running
   `pip install --upgrade google-api-python-client`
"""
from pprint import pprint

from googleapiclient import discovery

developerKey='AIzaSyCsb45b6AcwLQNNHE3sLyVHuNO4QF1IsU8'

service = discovery.build('compute', 'v1', developerKey='api_key')

# Project ID for this request.
project = 'esoteric-kiln-376000'  # TODO: Update placeholder value.

# The name of the zone for this request.
zone = 'asia-northeast1-b'  # TODO: Update placeholder value.

# instance_body = {
#     # TODO: Add desired entries to the request body.
# }

# request = service.instances().insert(project=project, zone=zone, body=instance_body)
# response = request.execute()

# # TODO: Change code below to process the `response` dict:
# pprint(response)

request = service.instances().list(project=project, zone=zone)
while request is not None:
    response = request.execute()

    for instance in response['items']:
        # TODO: Change code below to process each `instance` resource:
        pprint(instance)

    request = service.instances().list_next(previous_request=request, previous_response=response)

    