#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2023, Mark Mercado <mmercado@digitalocean.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: account_info
short_description: Show information about the current user account
version_added: 0.1.0
description:
  - Show information about the current user account.
  - View the API documentation at U(https://docs.digitalocean.com/reference/api/api-reference/#operation/account_get).
author: Mark Mercado (@mamercad)
requirements:
  - pydo >= 0.1.3
  - azure-core >= 1.26.1
extends_documentation_fragment:
  - digitalocean.cloud.common.documentation
"""


EXAMPLES = r"""
- name: Get account information
  digitalocean.cloud.account_info:
"""


RETURN = r"""
account:
  description: Account information.
  returned: always
  type: dict
  sample:
    droplet_limit: 25
    floating_ip_limit: 5
    email: sammy@digitalocean.com
    uuid: b6fr89dbf6d9156cace5f3c78dc9851d957381ef
    email_verified": true,
    status: active
    status_message: ' '
    team:
      uuid: 5df3e3004a17e242b7c20ca6c9fc25b701a47ece
      name: My Team
error:
  description: DigitalOcean API error.
  returned: failure
  type: dict
  sample:
    Message: Informational error message.
    Reason: Unauthorized
    Status Code: 401
msg:
  description: Account information result.
  returned: always
  type: str
  sample:
    - Current account information
    - Current account information not found
"""

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.digitalocean.cloud.plugins.module_utils.common import (
    DigitalOceanOptions,
)

import traceback

HAS_AZURE_LIBRARY = False
AZURE_LIBRARY_IMPORT_ERROR = None
try:
    from azure.core.exceptions import HttpResponseError
except ImportError:
    AZURE_LIBRARY_IMPORT_ERROR = traceback.format_exc()
else:
    HAS_AZURE_LIBRARY = True

HAS_PYDO_LIBRARY = False
PYDO_LIBRARY_IMPORT_ERROR = None
try:
    from pydo import Client
except ImportError:
    PYDO_LIBRARY_IMPORT_ERROR = traceback.format_exc()
else:
    HAS_PYDO_LIBRARY = True


class AccountInformation:
    def __init__(self, module):
        """Class constructor."""
        self.module = module
        self.client = Client(token=module.params.get("token"))
        self.state = module.params.get("state")
        if self.state == "present":
            self.present()

    def present(self):
        """Get the Account information."""
        try:
            account = self.client.account.get()
            account_info = account.get("account")
            if account_info:
                self.module.exit_json(
                    changed=False,
                    msg="Current account information",
                    account=account_info,
                )
            self.module.fail_json(
                changed=False, msg="Current account information not found"
            )
        except HttpResponseError as err:
            error = {
                "Message": err.error.message,
                "Status Code": err.status_code,
                "Reason": err.reason,
            }
            self.module.fail_json(changed=False, msg=error.get("Message"), error=error)


def main():
    argument_spec = DigitalOceanOptions.argument_spec()
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    if not HAS_AZURE_LIBRARY:
        module.fail_json(
            msg=missing_required_lib("azure.core.exceptions"),
            exception=AZURE_LIBRARY_IMPORT_ERROR,
        )
    if not HAS_PYDO_LIBRARY:
        module.fail_json(
            msg=missing_required_lib("pydo"),
            exception=PYDO_LIBRARY_IMPORT_ERROR,
        )

    AccountInformation(module)


if __name__ == "__main__":
    main()
