####################################
# create a instance with V2ray
####################################

import json
import instance_insert, create_firewall

project = 'persuasive-zoo-436506-v8'

# us-west4-b(Las Vegas)|asia-northeast1-b(Tokyo)|asia-east2-a(Hong Kong)
zone = 'asia-northeast1-b'

# Images list https://cloud.google.com/compute/docs/images/os-details
image_project = 'ubuntu-os-cloud'
image_family = 'ubuntu-2004-lts'

image = instance_insert.get_image_from_family(
    project=image_project, family=image_family)

# image_url=f"projects/{image_project}/global/images/{image.name}"
image_url = image.self_link

# pd-standard|pd-ssd|pd-balanced|pd-extreme
disk_type = 'zones/' + zone + '/diskTypes/pd-ssd'
disk_size_gb = 10
disks = [instance_insert.disk_from_image(
    disk_type, disk_size_gb, True, image_url, True)]

# e2-standard-2 (2 vCPU, 8 GB memory) | e2-small (2 vCPU, 2 GB memory)
type_name = 'e2-small'
machine_type = f"zones/{zone}/machineTypes/{type_name}"

instance_name = 'v2rayfromapitest11'
instance = instance_insert.create_instance(project_id=project, zone=zone,
                                           instance_name=instance_name, disks=disks, machine_type=machine_type, external_access=True)

external_ip = instance.network_interfaces[0].access_configs[0].nat_i_p


# Set instance network tags
tags_fingerprint = instance.tags.fingerprint
tags = ["v2ray", "http-server", "https-server"]
instance_insert.set_network_tags(
    project=project, zone=zone, instance_name=instance_name, networktags=tags, fingerprint=tags_fingerprint)

# Build startup script
# import os
# print(os.getcwd())
f = open('host/bat/config.json')
conf = json.load(f)
# print(conf["inbounds"][0]["port"])
# print(conf["inbounds"][0]["settings"]["clients"][0]["id"])
port = conf["inbounds"][0]["port"]
confstr = json.dumps(conf)
startupscript = \
    "#! /bin/bash\n"\
    "bash <(curl -L https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-release.sh)\n"\
    "cat <<EOL >/usr/local/etc/v2ray/config.json\n"\
    f"{confstr}\n"\
    "EOL\n"\
    "systemctl start v2ray\n"\
    "systemctl enable v2ray\n"\
    "echo 'net.core.default_qdisc=fq' >>/etc/sysctl.conf\n"\
    "echo 'net.ipv4.tcp_congestion_control=bbr' >>/etc/sysctl.conf\n"\
    "sysctl -p"

metadata_fingerprint = instance.metadata.fingerprint
instance_insert.set_startup_script(
    project=project, zone=zone, instance_name=instance_name, script=startupscript, fingerprint=metadata_fingerprint)
# TODO: clear startup script
# metadata_fingerprint = instance.metadata.fingerprint
# instance_insert.set_startup_script(
#     project=project, zone=zone, instance_name=instance_name, script='wtf', fingerprint=metadata_fingerprint)

# rule_name='v2rayfromapi2'
# create_firewall.create_firewall_rule(project_id=project, firewall_rule_name=rule_name)

print(f'V2ray address: {external_ip}')
print(f'V2ray port: {port}')
