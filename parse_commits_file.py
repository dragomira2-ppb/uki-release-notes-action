from datetime import datetime
import re
import base64
from validate_env_variables import ENV_VARIABLES

def parse_commit_data():
    input_release_commits = base64.b64decode(ENV_VARIABLES['COMMIT_MESSAGE_ENCODED']).decode('utf-8')

    commit_data_list = []
    commit_pattern = re.compile(
        r'commit (\S+)\@Author: (.*?)\@Date:\s+([^\@]+)\@\@(.*?)(?=\@commit|\Z)', re.DOTALL)

    for match in commit_pattern.finditer(input_release_commits):
        commit_data = {
            "commit": match.group(1),
            "author": (re.compile(r'<(.*?)>').findall(match.group(2)))[0],
            "date": datetime.strptime(match.group(3), "%a %b %d %H:%M:%S %Y %z").strftime("%d %b %Y - %H:%M"),
            "commit_message": match.group(4).strip(),
        }
        commit_data_list.append(commit_data)

    return commit_data_list