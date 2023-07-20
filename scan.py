import os
import git
from pathlib import Path
import json
from pygments import highlight, lexers, formatters

GIST_PATH = str(Path.home()) + '/gist/'
GIT_PATH = str(Path.home()) + '/github/'


def print_json_data(data):
    formatted = json.dumps(data, sort_keys=True, indent=4)
    colorized = highlight(
        formatted,
        lexers.JsonLexer(),
        formatters.TerminalFormatter()
    )
    print(colorized)


def get_folders():
    git_dirs = os.listdir(GIT_PATH)
    gist_dirs = os.listdir(GIST_PATH)

    git_checked = list(map(lambda item: {
        'name': item,
        'path': GIT_PATH + item,
        'commited': git.Repo(GIT_PATH+item).git.status(),
    }, git_dirs))

    print_json_data(json.loads(json.dumps(git_checked)))


try:
    if (Path(GIST_PATH).exists() and Path(GIT_PATH).exists()):
        get_folders()
    else:
        print('Folder not found!')
except FileExistsError:
    print('Error!')
