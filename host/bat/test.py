import os

import requests
import json
import instance_insert
from google.cloud import compute_v1
from typing import Any

project = 'esoteric-kiln-376000'

# us-west4-b(Las Vegas)|asia-northeast1-b(Tokyo)|asia-east2-a(Hong Kong)
zone = 'asia-northeast1-b'
instance_name = 'v2rayfromapi'
# import os
# print(os.getcwd())
f=open('host/bat/config.json')
conf=json.load(f)
print(conf["inbounds"][0]["port"])
print(conf["inbounds"][0]["settings"]["clients"][0]["id"])
confstr=json.dumps(conf)
startupscript = \
    "#! /bin/bash\n"\
    "bash <(curl -L https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-release.sh)\n"\
    "cat <<EOL >/usr/local/etc/v2ray/config.json\n"\
    f"{confstr}\n"\
    "EOL\n"\
    "systemctl start v2ray\n"\
    "systemctl enable v2ray"
    # TODO: enable bbr
instance_insert.set_startup_script(
    project=project, zone=zone, instance_name=instance_name, script=startupscript)
