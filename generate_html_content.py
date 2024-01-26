from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from utils import ENV_VARIABLES

def generate_info_table():
    
    table_data = {
        'TLA': ENV_VARIABLES['TLA_NAME'],
        'Environment': ENV_VARIABLES['ENVIRONMENT'],
        'Brand' : ENV_VARIABLES['BRAND'],
        'Build number': ENV_VARIABLES['BUILD_NUMBER'],
        'Release date': datetime.now().strftime("%d %b %Y - %H:%M:%S"),
        'Repository': f'<a href="{ENV_VARIABLES["REPOSITORY"]}">{ENV_VARIABLES["TLA_NAME"]} - Repository</a>'
    }

    html_table = ''

    for key, value in table_data.items():
        html_table += f'<tr><th>{key}</th><td>{value}</td></tr>'

    return html_table

def generate_commits_table(data):
    table_header = '<tr><th>Commit ref</th><th>Author</th><th>Date</th><th>Commit message</th></tr>'
    table_data = []

    for entry in data:
        commit_link =  f'<a href="{ENV_VARIABLES["REPOSITORY"]}/commit/{entry["commit"]}">#{entry["commit"][:7]}</a>'
        commit_lines = entry['commit_message'].split('\n')
        commit_message_formatted = ''.join('- ' + line.strip() + '<br/><br/>' for line in commit_lines[:-1]) + '- ' + commit_lines[-1].strip()
        table_data.append(
        f'<tr><td style="text-align: center">{commit_link}</td><td style="text-align: center">{entry["author"]}</td><td style="text-align: center">{entry["date"]}</td><td>{commit_message_formatted}</td></tr>'
        )

    return table_header + ''.join(table_data)

def generate_html_content(data):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template.html')

    html_content = template.render(
        APPLICATION_NAME=ENV_VARIABLES['APPLICATION_NAME'],
        RELEASE_NAME=ENV_VARIABLES['RELEASE_NAME'],
        application_info_table=''.join(generate_info_table()),
        commits_table=generate_commits_table(data)
    )

    return html_content