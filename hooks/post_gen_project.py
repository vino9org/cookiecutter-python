import json
import os
import shlex
import shutil
import subprocess

context = json.loads(
    """
{{ cookiecutter | jsonify }}
"""
)

dockerfile_option = context["dockerfile_option"]
extra_packages = context["extra_packages"]
pkg_name = context["pkg_name"]

if dockerfile_option == "None":
    # none
    shutil.rmtree(".github")
    os.unlink("Dockerfile")
    os.unlink(".dockerignore")
elif dockerfile_option == "Dockerfile only":
    shutil.rmtree(".github")
else:
    # dockerfile and github workflow
    print(
        """
    Github workflow has been generated under .github/workflows directory. To create the corresponding
    Github repository, please run the following command:

        cd {{ cookiecutter.project_slug }}
        gh repo create {{ cookiecutter.project_slug }} --source=. --public
        git push -u origin develop

    Please ensure the workflow permission is seting to 'Read and write permissions' to enable pushing
    container images to Github container registry.

    """
    )

if "sqlalchemy" not in extra_packages:
    os.unlink(f"{pkg_name}/models.py")
    os.unlink("tests/test_models.py")
    os.unlink("alembic.ini")
    shutil.rmtree("migrations")

# create a git repo, everybody needs this, right?
print("Initializing git repo...")
subprocess.call(shlex.split("git init"))
subprocess.call(shlex.split("git checkout -b develop"))
subprocess.call(shlex.split("git add .gitignore .flake8 .dockerignore"))
subprocess.call(shlex.split("git add *"))
subprocess.call(shlex.split('git commit -m "generated by cookiecutter"'), stdout=subprocess.DEVNULL)

# print some help messages
home = os.path.expanduser("~")
relpath = os.path.relpath(os.getcwd(), home)
print(
    f"""
    # To start working on the project,

    cd ~/{relpath}

    """
)

print(
    """

    poetry install --no-root
    poettry export -f requirements.txt -o requirements.txt --without-hashes
    poettry export -f requirements.txt --group dev -o requirements-dev.txt --without-hashes
    poetry shell

    # under poetry, run the following commands to install linting tools
    pre-commit install
    flake8

    # Hack away!

    """
)
