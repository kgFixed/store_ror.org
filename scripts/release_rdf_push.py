import os
from pathlib import Path
from git_commit_push import git_push_existing_ttl
from template_to_try import process_ror_file

def version_key(version_str):
    version_parts = version_str[1:].split('.')
    return tuple(int(part) if part.isdigit() else 0 for part in version_parts)

def list_json_files_in_releases(releases_root, output_dir):

    release_folders = [d for d in os.listdir(releases_root) 
                      if os.path.isdir(os.path.join(releases_root, d)) and d.startswith('v')]
    
    release_folders.sort(key=version_key)

    for release in release_folders:
        release_path = os.path.join(releases_root, release)

        print(f"\n=== Release processing {release} ===")
        json_files = [f for f in os.listdir(release_path) if f.endswith('.json')]

        if not json_files:
            print(f"No JSON files found in {release}")
        else:
            print("JSON files found:")
            for json_file in json_files:
                json_path = os.path.join(release_path, json_file)
                print(f"File processing: {json_path}")

                process_ror_file(json_path, output_dir)

        if release != release_folders[-1]:
            print("\nWait for the commit and push files...")
            success = git_push_existing_ttl(
                repo_dir= Path(__file__).parent.parent,
                target_dir= "folder_to_push",
                version_name=f"Release {release}",
                tag_version=f"{release}"
            )

            if not success:
                print("\n✗ Operation failed. See messages above.")
                exit(1)
            
            print(f"\n✓ Release {release} pushed successfully!")

if __name__ == "__main__":
    root_dir = Path(__file__).parent.parent
    releases_dir = root_dir / "ror_releases"
    output_dir = root_dir / "folder_to_push"
    
    if not releases_dir.exists():
        print(f"Error: The {releases_dir} folder does not exist")
    else:
        list_json_files_in_releases(releases_dir, output_dir)