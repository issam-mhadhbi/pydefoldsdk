from setuptools import setup, find_packages
import os
import subprocess

class PypiPublisher:
    def __init__(self, start_version="1.0.0"):
        self.start_version = start_version
        self.name = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            capture_output=True, text=True
        ).stdout.strip().split("/")[-1].replace(".git", "")
        print(f"Project name: {self.name}")

        self.version, self.new_version = self.get_versions()
        print(f"Project version: {self.version} -> {self.new_version}")

        author = (
            os.environ.get("GITLAB_USER_NAME") or
            subprocess.check_output(['git', 'config', 'user.name']).decode().strip()
        )

        author_email = (
            os.environ.get("GITLAB_USER_EMAIL") or
            subprocess.check_output(['git', 'config', 'user.email']).decode().strip()
        )

        url = (
            os.environ.get("CI_PROJECT_URL") or
            subprocess.check_output(['git', 'remote', 'get-url', 'origin']).decode().strip()
        )

        description = (
            os.environ.get("CI_PROJECT_DESCRIPTION") or
            "Python Package made by Mhadhbi Issam."
        )

        # Read requirements.txt
        install_requires = self.get_requirements()

        setup(
            name=os.path.basename(os.getcwd()),
            version=os.environ.get("DEFOLD_SDK_VERSION"),
            packages=find_packages(exclude=["docs", "docs.*",".readthedocs.yaml"]),
            author=author,
            author_email=author_email,
            description=description,
            long_description=open("README.md").read(),
            long_description_content_type="text/markdown",
            url=url,
            install_requires=install_requires,
            classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
            ],
        )

    def get_requirements(self):
        """Read requirements.txt and return a list of dependencies."""
        req_file = os.path.join(os.getcwd(), "requirements.txt")
        if not os.path.exists(req_file):
            return []
        with open(req_file, "r") as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        return lines

    def get_versions(self):
        """Stub for getting current and new version."""
        # Replace with your logic
        return self.start_version, self.start_version

if __name__ == "__main__":
    PypiPublisher()