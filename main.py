import os
import json
import tempfile
import shutil
import logging
from git import Repo
from urllib.parse import urlparse

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


class GitRepoToJson:

    def __init__(self, repo_url: str):
        self.repo_url = repo_url
        self.repo_dir = None
        self.repo = None
        self.repo_name = self.get_repo_name()

    def get_repo_name(self):
        """
        Extract the repository name from the URL.
        """
        parsed_url = urlparse(self.repo_url)
        repo_name = os.path.basename(parsed_url.path)
        return repo_name

    def clone_repo(self):
        """
        Clone the GitHub repository to a temporary directory.
        """
        self.repo_dir = tempfile.mkdtemp()
        logging.info(f"Cloning repository from {self.repo_url} into {self.repo_dir}")
        self.repo = Repo.clone_from(self.repo_url, self.repo_dir)

    def parse_files(self):
        """
        Recursively parse all non-hidden files and directories, excluding .git and hidden system files.
        Returns a list of file info dictionaries.
        """
        file_list = []
        logging.info("Scanning files in the repository...")

        for root, dirs, files in os.walk(self.repo_dir):
            # Exclude hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for file in files:
                if file.startswith('.'):
                    continue  # Skip hidden files

                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, self.repo_dir)

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except Exception as e:
                    logging.warning(f"Could not read file {file_path}: {e}")
                    content = ""

                file_list.append({
                    "filename": file,
                    "path": relative_path.replace("\\", "/"),  # Normalize Windows paths
                    "content": content
                })

        logging.info(f"Found {len(file_list)} files.")
        return file_list

    def write_to_json(self, data):
        """
        Write collected file data to a JSON file.
        The JSON file name will include the repository name.
        """
        output_file = f"{self.repo_name}.json"
        logging.info(f"Writing data to {output_file}")
        try:
            with open(output_file, "w", encoding='utf-8') as json_file:
                json.dump(data, json_file, indent=2, ensure_ascii=False)
            logging.info("JSON file successfully written.")
        except Exception as e:
            logging.error(f"Failed to write JSON file: {e}")

    def clean_up(self):
        """
        Delete the temporary cloned repository directory.
        """
        if self.repo:
            del self.repo  # Release file handles
        if self.repo_dir:
            shutil.rmtree(self.repo_dir, ignore_errors=True)
            logging.info("Temporary repository directory cleaned up.")

    def run(self):
        """
        Main execution method.
        """
        try:
            self.clone_repo()
            data = self.parse_files()
            self.write_to_json(data)
        finally:
            self.clean_up()


if __name__ == '__main__':
    repo_url = input("Enter GitHub repository URL: ").strip()
    converter = GitRepoToJson(repo_url)
    converter.run()
