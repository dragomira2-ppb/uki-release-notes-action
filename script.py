from generate_html_content import generate_html_content
from parse_commits_file import parse_commit_data
from publish_to_confluence import publish_page_to_confluence

import logging

from validate_env_variables import are_confluence_vars_valid, are_mandatory_vars_valid

def main():
      if are_mandatory_vars_valid() == True:
          commit_data = parse_commit_data()
          html_content = generate_html_content(commit_data)
          if are_confluence_vars_valid() == True:
              publish_page_to_confluence(html_content)

if __name__ == "__main__":
    main()