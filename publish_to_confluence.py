import requests
from validate_env_variables import ENV_VARIABLES
from validate_env_variables import publish_page_to_confluence

def publish_page_to_confluence(html_content):

    if publish_page_to_confluence == True:

        api_endpoint = "/rest/api/content"
    
        #modifying existing page for testing purposes
        new_page_payload = {
            "id" : ENV_VARIABLES['CONFLUENCE_EXISTING_PAGE'],
            "type": "page",
            "title": ENV_VARIABLES['TLA_NAME'] + ' ' + ENV_VARIABLES['BRAND'] + ' ' + ENV_VARIABLES['RELEASE_NAME'],
            "space":{
                  "key": ENV_VARIABLES['CONFLUENCE_SPACE']
             },
            "body": {
                "storage": {
                    "value": f"{html_content}",
                    "representation": "storage",
                }
            },
            "version": {
                "number":  ENV_VARIABLES['CONFLUENCE_PAGE_VERSION']
            }
        }
    
        # Headers for authentication
        headers = {
            "Content-Type": "application/json",
            "X-Atlassian-Token": "no-check"
        }
    
        response = requests.put(f"{ENV_VARIABLES['CONFLUENCE_URL']}{api_endpoint}/{ENV_VARIABLES['CONFLUENCE_EXISTING_PAGE']}",headers=headers, json=new_page_payload, auth=(ENV_VARIABLES['CONFLUENCE_USERNAME'], ENV_VARIABLES['CONFLUENCE_API_TOKEN']))
        if not "200" in response:
            raise ValueError(f"Error occured when calling Confluence REST API - {response}")