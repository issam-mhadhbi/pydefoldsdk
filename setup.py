from setuptools import setup, find_packages
import os
import subprocess


def safe_git_config(cmd, default=""):
    try:
        return subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return default


class PypiPublisher:
    def __init__(self, start_version="1.0.0"):
        self.start_version = start_version

        # Safe project name
        repo_url = safe_git_config(["git", "config", "--get", "remote.origin.url"])
        self.name = repo_url.split("/")[-1].replace(".git", "") if repo_url else os.path.basename(os.getcwd())
        print(f"Project name: {self.name}")

        self.version, self.new_version = self.get_versions()
        print(f"Project version: {self.version} -> {self.new_version}")

        # Safe metadata
        author = os.environ.get("GITLAB_USER_NAME") or safe_git_config(["git", "config", "user.name"], "Unknown")

        author_email = os.environ.get("GITLAB_USER_EMAIL") or safe_git_config(
            ["git", "config", "user.email"], "unknown@example.com"
        )

        url = os.environ.get("CI_PROJECT_URL") or safe_git_config(
            ["git", "remote", "get-url", "origin"], ""
        )

        description = os.environ.get("CI_PROJECT_DESCRIPTION") or "Python Package made by Mhadhbi Issam."

        # Read requirements
        install_requires = self.get_requirements()

        setup(
            name=self.name,
            version=os.environ.get("DEFOLD_SDK_VERSION", self.start_version),
            packages=find_packages(exclude=["docs", "docs.*"]),
            author=author,
            author_email=author_email,
            description=description,
            long_description=open("README.md").read() if os.path.exists("README.md") else "",
            long_description_content_type="text/markdown",
            url=url,
            project_urls={
                "Documentation": "https://pydefoldsdk.readthedocs.io",
                "Source": url,
                "Tracker": f"{url}/issues" if url else "",
            },
            install_requires=install_requires,  # ✅ fixed comma issue
            classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
            ],
        )

    def get_requirements(self):
        req_file = os.path.join(os.getcwd(), "requirements.txt")
        if not os.path.exists(req_file):
            return []
        with open(req_file, "r") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]

    def get_versions(self):
        return self.start_version, self.start_version


if __name__ == "__main__":
    PypiPublisher()