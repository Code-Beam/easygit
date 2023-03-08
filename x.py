import os
import sys
import re
import httpx
from termcolor import colored
import random


def is_github_repo(url):
    # Check if the URL matches the pattern for a GitHub repository
    github_repo_pattern = r"https?://github.com/([a-zA-Z0-9\-]+)/([a-zA-Z0-9\-]+)"
    match = re.match(github_repo_pattern, url)
    if match:
        return True
    else:
        return False

def download_github_repo(url):
    # Get the username and repository name from the URL
    github_repo_pattern = r"https?://github.com/([a-zA-Z0-9\-]+)/([a-zA-Z0-9\-]+)"
    match = re.match(github_repo_pattern, url)
    username = match.group(1)
    repo_name = match.group(2)
    # Create a session to make the HTTP requests
    with httpx.Client() as client:
        # Get the list of files in the repository
        response = client.get(f"https://api.github.com/repos/{username}/{repo_name}/contents")
        if response.status_code != 200:
            print("Error getting repository contents:", response.status_code)
            sys.exit(1)
        contents = response.json()
        # Create the directory to store the repository files
        repo_dir = os.path.join(os.getcwd(), repo_name)
        os.makedirs(repo_dir, exist_ok=True)
        # Download each file in the repository
        for item in contents:
            if item["type"] == "file":
                response = client.get(item["download_url"])
                if response.status_code != 200:
                    print(f"Error downloading file {item['name']}: {response.status_code}")
                else:
                    with open(os.path.join(repo_dir, item["name"]), "wb") as f:
                        my_list = ["red", "green", "blue", "yellow", "white"]
                        colorstr = random.choice(my_list)
                        f.write(response.content)
                        print(colored(f"Downloaded file {item['name']}",colorstr))

        print(colored(f"DOWNLOADED ALL THE FILES 🎉",'white'))            

if __name__ == "__main__":
    if os.name == 'nt': 
        os.system('cls')
    else:  
        os.system('clear')

    intro = """
                ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄   ▄▄    ▄▄▄▄▄▄▄ ▄▄▄ ▄▄▄▄▄▄▄ 
                █       █       █       █  █ █  █  █       █   █       █
                █    ▄▄▄█   ▄   █  ▄▄▄▄▄█  █▄█  █  █   ▄▄▄▄█   █▄     ▄█
                █   █▄▄▄█  █▄█  █ █▄▄▄▄▄█       █  █  █  ▄▄█   █ █   █  
                █    ▄▄▄█       █▄▄▄▄▄  █▄     ▄█  █  █ █  █   █ █   █  
                █   █▄▄▄█   ▄   █▄▄▄▄▄█ █ █   █    █  █▄▄█ █   █ █   █  
                █▄▄▄▄▄▄▄█▄▄█ █▄▄█▄▄▄▄▄▄▄█ █▄▄▄█    █▄▄▄▄▄▄▄█▄▄▄█ █▄▄▄█  


    """

    print(colored(intro, 'blue'))

    url = input("Enter a GitHub repository URL: ")

    if not is_github_repo(url):

        print("Invalid GitHub repository URL")

        sys.exit(1)

    download_github_repo(url)
