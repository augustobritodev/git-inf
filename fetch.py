# Install Requirements
# python3 -m pip install -r requests
# python3 -m pip install -r pygmments

import sys
import datetime
import requests
import json
from pygments import highlight, lexers, formatters
import os

menuTitleText = """
 _______  _______  _______  _______  __   __    _______  ___   _______  __   __  __   __  _______
|       ||       ||       ||       ||  | |  |  |       ||   | |       ||  | |  ||  | |  ||  _    |
|    ___||    ___||_     _||       ||  |_|  |  |    ___||   | |_     _||  |_|  ||  | |  || |_|   |
|   |___ |   |___   |   |  |       ||       |  |   | __ |   |   |   |  |       ||  |_|  ||       |
|    ___||    ___|  |   |  |      _||       |  |   ||  ||   |   |   |  |       ||       ||  _   |
|   |    |   |___   |   |  |     |_ |   _   |  |   |_| ||   |   |   |  |   _   ||       || |_|   |
|___|    |_______|  |___|  |_______||__| |__|  |_______||___|   |___|  |__| |__||_______||_______|

                                    Writen by: Augusto Brito

                    Instructions

                    1.0) Choose your search type:
                        1.) Type for 1 - Public or for 2 - Private
                    2.0) If you select Private, you need to authenticate via GitHub Token.
                    3.0) Type 3 for exit.
"""

userInfoText = """
 __   __  _______  _______  ______      ___   __    _  _______  _______
|  | |  ||       ||       ||    _ |    |   | |  |  | ||       ||       |
|  | |  ||  _____||    ___||   | ||    |   | |   |_| ||    ___||   _   |
|  |_|  || |_____ |   |___ |   |_||_   |   | |       ||   |___ |  | |  |
|       ||_____  ||    ___||    __  |  |   | |  _    ||    ___||  |_|  |
|       | _____| ||   |___ |   |  | |  |   | | | |   ||   |    |       |
|_______||_______||_______||___|  |_|  |___| |_|  |__||___|    |_______|

"""

reposText = """
 ______    _______  _______  _______  _______
|    _ |  |       ||       ||       ||       |
|   | ||  |    ___||    _  ||   _   ||  _____|
|   |_||_ |   |___ |   |_| ||  | |  || |_____
|    __  ||    ___||    ___||  |_|  ||_____  |
|   |  | ||   |___ |   |    |       | _____| |
|___|  |_||_______||___|    |_______||_______|

"""

USER_NAME = 'augustobrit'
USER_TOKEN = ''
GITHUB_API_URL = 'https://api.github.com'

update = True
userInput = 0
userToken = USER_TOKEN  # USE .env TOKEN FOR DEFAULT VALUE
searchInput = 1


def main():
    print(menuTitleText)

    while update == True:

        try:
            userInput = int(input("Search Type: "))

            if userInput == 1:
                print("Public Search")
                searchInput = 1
                global data
                data = get_user_data()
                if (data != None):
                    print_json_data(data)
                    current_dir = os.path.dirname(os.path.realpath(__file__))
                    export_data(current_dir + '/teste', data, 'file')
            elif userInput == 2:
                print("Private Search")
                # userToken = input("Type Github USER TOKEN: ")
                print('Not implemented yet')
                exit()
                searchInput = 2
            elif userInput == 3:
                clear()
            elif userInput == 4:
                print("Exiting...")
                exit()
                searchInput = 4
            else:
                print("Invalid option! ")
        except ValueError:
            print("Type an option between 1-3")
            userInput = 0

        # data = get_repos_data()


def get_user_data():
    user = {}
    if searchInput == 1:
        try:
            response = requests.get(
                url=GITHUB_API_URL + '/users/' + USER_NAME
            )
        except Exception:
            print('Error fetching data from github.')
    elif searchInput == 2:
        response = requests.get(
            url=GITHUB_API_URL + '/user',
            auth=(USER_NAME, USER_TOKEN)
        )

    if (response.ok):
        user = response.json()
        return {
            'name': user['name'],
            'bio': user['bio'],
            'followers': user['followers'],
            'following': user['following'],
            'location': user['location'],
            'gists': user['public_gists'],
            'repos': user['public_repos'],
            'url': user['html_url'],
        }


def get_repos_data():
    repos = []
    try:
        response = requests.get(
            url=GITHUB_API_URL + '/users/' + USER_NAME + '/repos'
        )
    except Exception:
        print("Error fetching repository data from GitHub.")

    if (response.ok):
        repos = response.json()
        return list(
            map(lambda repo: {
                'name': repo['name'],
                'description': repo['description'],
                'size': repo['size'],
                'created': repo['created_at'],
                'updated': repo['updated_at'],
                'url': repo['html_url'],
                'git': repo['git_url'],
            },
                repos
            )
        )


def print_json_data(data):
    formatted = json.dumps(data, sort_keys=True, indent=4)
    colorized = highlight(
        formatted,
        lexers.JsonLexer(),
        formatters.TerminalFormatter()
    )
    print(colorized)


def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


def export_data(path, data, file_name):
    print(is_valid(path))
    # with open(file_name + '.json', 'w') as outfile:
    #json.dump(data, outfile, sort_keys=True, indent=4)


def import_data():
    print('not implement yet')


def is_valid(path):
    if not os.access(path, os.W_OK):
        try:
            open(path, 'w').close()
            os.unlink(path)
            return True
        except OSError:
            print('Path is not valid.')
            return False


main()
