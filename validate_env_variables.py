import os
import logging
import base64

ENV_VARIABLES = {
    # application env variables
    'APPLICATION_NAME': os.environ.get('APPLICATION_NAME', ''),
    'REPOSITORY': os.environ.get('REPOSITORY', ''),
    'TLA_NAME': os.environ.get('TLA_NAME', ''),
    'BRAND': os.environ.get('BRAND', ''),
    'ENVIRONMENT': os.environ.get('ENVIRONMENT', ''),

    # release details env variables
    'COMMIT_MESSAGE': base64.b64decode(os.environ.get('COMMIT_MESSAGE_ENCODED', '')).decode('utf-8'),
    'RELEASE_NAME': os.environ.get('RELEASE_NAME', ''),
    'BUILD_NUMBER': os.environ.get('BUILD_NUMBER', '')
}

CONFLUENCE_VARS = {

    'CONFLUENCE_USERNAME': os.environ.get('CONFLUENCE_USERNAME', ''),
    'CONFLUENCE_URL': os.environ.get('CONFLUENCE_URL', ''),
    'CONFLUENCE_PAGE_ID': os.environ.get('CONFLUENCE_PAGE_ID', ''),
    'CONFLUENCE_SPACE': os.environ.get('CONFLUENCE_SPACE', ''),
    'CONFLUENCE_API_TOKEN': os.environ.get('CONFLUENCE_API_TOKEN', ''),

    # for testing purposes
    'CONFLUENCE_EXISTING_PAGE': os.environ.get('CONFLUENCE_EXISTING_PAGE', ''),
    'CONFLUENCE_PAGE_VERSION': os.environ.get('CONFLUENCE_PAGE_VERSION', '')
}

# Setting basic logging config
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    handlers=[logging.StreamHandler()])

"""
    Validate the values of environment variables.
    If any value is empty or None, raise an error.
    
    Confluence variables are optional, if one of them is not provided, confluence integration will not be executed.
"""


def are_confluence_vars_valid():
    publish_to_confluence = True
    for key, value in CONFLUENCE_VARS.items():
        if not value:
            # Confluence variables are optional, log a warning if empty
            warning_message = f"Warning: {key} is empty or None. Confluence integration will not execute."
            logging.warning(warning_message)
            publish_to_confluence = False

    logging.info('Confluence variables are present.')
    return publish_to_confluence


def are_mandatory_vars_valid():

    for key, value in ENV_VARIABLES.items():
        if not value:
            error_message = f"Error: {key} cannot be empty or None."
            raise ValueError(error_message)

    logging.info('All values are present.')
    return True