import requests
import json
import samples
from google.cloud import compute_v1
from typing import Any

project = 'esoteric-kiln-376000'
# us-west4-b(Las Vegas)|asia-northeast1-b(Tokyo)|asia-east2-a(Hong Kong)
zone = 'asia-east2-a'

# Images list https://cloud.google.com/compute/docs/images/os-details
image_project = 'ubuntu-os-cloud'
image_family = 'ubuntu-1804-lts'

image = samples.get_image_from_family(
    project=image_project, family=image_family)

# image_url=f"projects/{image_project}/global/images/{image.name}"
image_url = image.self_link

# pd-standard|pd-ssd|pd-balanced|pd-extreme
disk_type = 'zones/' + zone + '/diskTypes/pd-balanced'
disk_size_gb = 40
disks = [samples.disk_from_image(
    disk_type, disk_size_gb, True, image_url, True)]

# e2-standard-2 (2 vCPU, 8 GB memory) | e2-small (2 vCPU, 2 GB memory)
type_name = 'e2-standard-2'
machine_type = f"zones/{zone}/machineTypes/{type_name}"

instance_name = 'frompythonapi'
instance = samples.create_instance(project_id=project, zone=zone,
                                   instance_name=instance_name, disks=disks, machine_type=machine_type, external_access=True)

# print(d)
# samples.create_firewall_rule(project_id=project,firewall_rule_name="test")
print(
    f'External IP:{instance.network_interfaces[0].access_configs[0].nat_i_p}')

# Set metadata https://cloud.google.com/python/docs/reference/compute/latest/google.cloud.compute_v1.services.instances.InstancesClient?hl=en#google_cloud_compute_v1_services_instances_InstancesClient_set_metadata
fingerprint = instance.metadata.fingerprint
body = {
    "items": [{
        "key": "startup-script",
        "value": "#! /bin/bash\napt update\napt -y install apache2\ncat <<EOF > /var/www/html/index.html\n<html><body><p>Linux startup script added directly.</p></body></html>\nEOF"
    }],
    "fingerprint": fingerprint
}

request = compute_v1.SetMetadataInstanceRequest()
request.zone = zone
request.project = project
request.instance = instance_name
request.metadata_resource = body
compute_v1.InstancesClient().set_metadata(request=request)

# Set tags https://cloud.google.com/python/docs/reference/compute/latest/google.cloud.compute_v1.services.instances.InstancesClient?hl=en#google_cloud_compute_v1_services_instances_InstancesClient_set_tags
fingerprint = instance.metadata.fingerprint
body = {
    "items": [
        "netch",
        "http-server",
        "https-server"
    ],
    "fingerprint": fingerprint
}
request = compute_v1.SetTagsInstanceRequest()
request.zone = zone
request.project = project
request.instance = instance_name
request.tags_resource = body
compute_v1.InstancesClient().set_tags(request=request)

samples.delete_instance(project, zone, instance_name)

print("done")
