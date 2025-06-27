import os
from pathlib import Path
import requests

def release_version_ror(releases_root):
    release_folders = [d for d in os.listdir(releases_root) 
                        if os.path.isdir(os.path.join(releases_root, d)) and d.startswith('v')]
    
    return release_folders

def get_github_releases(repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases?per_page=100"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  
        
        releases = response.json()
        release_tags = [release['tag_name'] for release in releases]
        
        return release_tags
    
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête: {e}")
        return []
    
def compare_release(releases_version_local, releases_version_remote):
    elements_diff = list(set(releases_version_local) ^ set(releases_version_remote))

    return elements_diff


if __name__ == "__main__":

    repo_owner = "ror-community"
    repo_name = "ror-records"
    root_dir = Path(__file__).parent.parent
    releases_dir = root_dir / "ror_releases"

    releases_local = release_version_ror(releases_dir)
    releases_remote = get_github_releases(repo_owner, repo_name)

    diff = compare_release(releases_local, releases_remote)
    
    print(diff)