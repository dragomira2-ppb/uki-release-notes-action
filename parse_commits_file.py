from datetime import datetime
import re
from utils import ENV_VARIABLES

def parse_commit_data():
    with open(ENV_VARIABLES['RELEASE_LOG_FILE_PATH'], 'r') as file:
        input_text = file.read()

    commit_data_list = []
    commit_pattern = re.compile(
        r'commit (\S+)\nAuthor: (.*?)\nDate:\s+([^\n]+)\n\n(.*?)(?=\n\ncommit|\Z)', re.DOTALL)

    for match in commit_pattern.finditer(input_text):
        commit_data = {
            "commit": match.group(1),
            "author": (re.compile(r'<(.*?)>').findall(match.group(2)))[0],
            "date": datetime.strptime(match.group(3), "%a %b %d %H:%M:%S %Y %z").strftime("%d %b %Y - %H:%M"),
            "commit_message": match.group(4).strip(),
        }

        commit_data_list.append(commit_data)

    return commit_data_list