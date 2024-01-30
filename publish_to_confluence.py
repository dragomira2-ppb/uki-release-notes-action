import requests
from validate_env_variables import ENV_VARIABLES, CONFLUENCE_VARS

import json
import logging


def publish_page_to_confluence(html_content):

    api_endpoint = "https://flutteruki.atlassian.net/wiki/rest/api/content"

    # modifying existing page for testing purposes
    new_page_payload = {
        "id": int(CONFLUENCE_VARS['CONFLUENCE_EXISTING_PAGE']),
        "type": "page",
        "title": ENV_VARIABLES['TLA_NAME'] + ' ' + ENV_VARIABLES['BRAND'] + ' ' + ENV_VARIABLES['RELEASE_NAME'],
        "space": {
            "key": CONFLUENCE_VARS['CONFLUENCE_SPACE']
        },
        "body": {
            "storage": {
                "value": f"{html_content}",
                "representation": "storage",
            }
        },
        "version": {
            "number":  int(CONFLUENCE_VARS['CONFLUENCE_PAGE_VERSION'])
        }
    }

    # Headers for authentication
    headers = {
        "Content-Type": "application/json",
        "X-Atlassian-Token": "no-check"
    }
    logging.info(f"Confluence input payload: {new_page_payload}")

    response = requests.put(f"{api_endpoint}/{CONFLUENCE_VARS['CONFLUENCE_EXISTING_PAGE']}",
                            headers=headers, json=new_page_payload, auth=(CONFLUENCE_VARS['CONFLUENCE_USERNAME'], CONFLUENCE_VARS['CONFLUENCE_API_TOKEN']))
    logging.info(f"Confluence REST API call invoked, response: {json.dumps(response.__dict__, indent=4, sort_keys=True)}")
    if not "200" in response:
        raise ValueError(
            f"Error occured when calling Confluence REST API - {response}")
