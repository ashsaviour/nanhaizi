from __future__ import annotations

import sys
import samples
from typing import Any

from google.api_core.extended_operation import ExtendedOperation
from google.cloud import compute_v1


def create_firewall_rule(
    project_id: str, firewall_rule_name: str, network: str = "global/networks/default"
) -> compute_v1.Firewall:
    """
    Creates a simple firewall rule allowing for incoming HTTP and HTTPS access from the entire Internet.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        firewall_rule_name: name of the rule that is created.
        network: name of the network the rule will be applied to. Available name formats:
            * https://www.googleapis.com/compute/v1/projects/{project_id}/global/networks/{network}
            * projects/{project_id}/global/networks/{network}
            * global/networks/{network}

    Returns:
        A Firewall object.
    """
    firewall_rule = compute_v1.Firewall()
    firewall_rule.name = firewall_rule_name
    firewall_rule.direction = "INGRESS"

    allowed_ports = compute_v1.Allowed()
    allowed_ports.I_p_protocol = "tcp"
    allowed_ports.ports = ["37881-37890"]

    firewall_rule.allowed = [allowed_ports]
    firewall_rule.source_ranges = ["0.0.0.0/0"]
    firewall_rule.network = network
    firewall_rule.description = "Allowing TCP traffic on port 37881 to 37890 from Internet."

    firewall_rule.target_tags = ["v2ray"]

    # Note that the default value of priority for the firewall API is 1000.
    # If you check the value of `firewall_rule.priority` at this point it
    # will be equal to 0, however it is not treated as "set" by the library and thus
    # the default will be applied to the new rule. If you want to create a rule that
    # has priority == 0, you need to explicitly set it so:
    # TODO: Uncomment to set the priority to 0
    # firewall_rule.priority = 0

    firewall_client = compute_v1.FirewallsClient()
    operation = firewall_client.insert(
        project=project_id, firewall_resource=firewall_rule
    )

    samples.wait_for_extended_operation(operation, "firewall rule creation")

    return firewall_client.get(project=project_id, firewall=firewall_rule_name)