from setuptools import setup, find_packages
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))

def safe_git_config(cmd, default=""):
    try:
        return subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return default

def get_project_name():
    repo_url = safe_git_config(["git", "config", "--get", "remote.origin.url"])
    if repo_url:
        return repo_url.split("/")[-1].replace(".git", "")
    return os.path.basename(os.getcwd())

def get_author():
    return "issam.mhadhbi.dev"

def get_author_email():
    return "issam.mhadhbi.dev@gmail.com"

def get_url():
    return (
        os.environ.get("CI_PROJECT_URL")
        or safe_git_config(["git", "remote", "get-url", "origin"], "")
    )

def get_description():
    return os.environ.get("CI_PROJECT_DESCRIPTION", "Python Package made by Mhadhbi Issam.")

def get_requirements():
    req_file = os.path.join(HERE, "requirements.txt")
    if not os.path.exists(req_file):
        return []
    with open(req_file, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

def read_readme():
    readme = os.path.join(HERE, "README.md")
    if os.path.exists(readme):
        with open(readme, encoding="utf-8") as f:
            return f.read()
    return ""

NAME         = get_project_name()
VERSION      = open(os.path.join(HERE, "VERSION")).read().strip()  # .strip() fixes newline
AUTHOR       = get_author()
AUTHOR_EMAIL = get_author_email()
URL          = get_url()
DESCRIPTION  = get_description()
REQUIREMENTS = get_requirements()
LONG_DESC    = read_readme()

setup(
    name=NAME,
    version=VERSION,
    packages=find_packages(exclude=["docs", "docs.*"]),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESC,
    package_data={"": ["VERSION"]},
    long_description_content_type="text/markdown",
    url=URL,
    project_urls={
        "Documentation": "https://pydefoldsdk.readthedocs.io",
        "Source": URL,
        "Tracker": f"{URL}/issues" if URL else "",
    },
    install_requires=REQUIREMENTS,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)