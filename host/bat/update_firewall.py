import requests,json
import samples
from google.cloud import compute_v1
from typing import Any

project = 'esoteric-kiln-376000'

def update_tcp_port(project: str = project, rule_name: str = "v2ray", ports: str = ["37880-37882"]) -> Any:
    ### update tcp port number

    firewall_rule = compute_v1.Firewall()
    allowed_ports = compute_v1.Allowed()
    allowed_ports.I_p_protocol = "tcp"
    allowed_ports.ports = ports
    firewall_rule.allowed = [allowed_ports]
    firewall_client = compute_v1.FirewallsClient()
    operation = firewall_client.patch(
        project=project, firewall=rule_name, firewall_resource=firewall_rule)
    res = samples.wait_for_extended_operation(
        operation, "firewall rule patching")
    return res

update_tcp_port(project=project)
print('done')