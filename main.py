from generate_html_content import generate_html_content
from parse_commits_file import parse_commit_data
from publish_to_confluence import publish_page_to_confluence
from utils import validate_env_variables
import logging

def main():
    try:
        validate_env_variables()
        logging.info("All env variables are valid")
        commit_data = parse_commit_data()
        html_content = generate_html_content(commit_data)
        publish_page_to_confluence(html_content)
    except ValueError as e:
        logging.error(str(e))

if __name__ == "__main__":
    main()