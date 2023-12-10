import os
import os.path
import shlex
import subprocess


def run_pytest_in_generated_project(project_path):
    if not os.path.isdir(project_path):
        return

    current_path = os.getcwd()

    try:
        os.chdir(project_path)
        subprocess.call(["poetry", "install"])
        assert subprocess.call(shlex.split("poetry run pytest -v")) == 0
    finally:
        os.chdir(current_path)


def run_flake8_in_generated_project(project_path):
    if not os.path.isdir(project_path):
        return

    current_path = os.getcwd()

    try:
        os.chdir(project_path)
        subprocess.call(["poetry", "install"])
        # run flake8 but ignore auto reformat of black (BLK100)
        # and blank lines related (E302, E303)
        assert (
            subprocess.call(
                shlex.split("poetry run flake8 -v --ignore BLK100,E302,E303,W291,W391")
            )
            == 0
        )
    finally:
        os.chdir(current_path)


def run_precommit_in_generated_project(project_path):
    if not os.path.isdir(project_path):
        return

    current_path = os.getcwd()

    try:
        os.chdir(project_path)
        subprocess.call(["poetry", "install"])
        assert subprocess.call(shlex.split("poetry run pre-commit install")) == 0
        with open("a.py", "w") as f:
            f.write("# just some text\n")
            f.write("some_var = 0\n")
        assert subprocess.call(shlex.split("git add a.py")) == 0
        assert subprocess.call(shlex.split("poetry run pre-commit run")) == 0
    finally:
        os.chdir(current_path)


def test_default_project(cookies):
    result = cookies.bake(
        extra_context={
            "project_name": "My Default Project",
        }
    )

    assert result.exit_code == 0
    assert result.exception is None

    assert result.project_path.name == "my-default-project"
    assert result.project_path.is_dir()
    assert (result.project_path / ".git/HEAD").is_file()

    print(f"\ntest project generated {result.project_path}")

    run_pytest_in_generated_project(result.project_path)
    run_flake8_in_generated_project(result.project_path)
    # run_precommit_in_generated_project(result.project_path)


def test_project_with_pandas(cookies):
    result = cookies.bake(
        extra_context={
            "project_name": "My Data Project",
            "extra_packages": "Install pandas 2.0.3",
        }
    )

    assert result.exit_code == 0
    assert result.exception is None

    assert result.project_path.name == "my-data-project"
    assert result.project_path.is_dir()
    assert (result.project_path / ".git/HEAD").is_file()

    print(f"\ntest project generated {result.project_path}")

    run_pytest_in_generated_project(result.project_path)
    run_flake8_in_generated_project(result.project_path)
    # run_precommit_in_generated_project(result.project_path)


def test_project_with_sqlalchemy(cookies):
    result = cookies.bake(
        extra_context={
            "project_name": "Database Project",
            "extra_packages": "Install sqlalchemy and alembic with postgresql driver",
        }
    )

    assert result.exit_code == 0
    assert result.exception is None

    assert result.project_path.name == "database-project"
    assert result.project_path.is_dir()
    assert (result.project_path / ".git/HEAD").is_file()

    print(f"\ntest project generated {result.project_path}")

    run_pytest_in_generated_project(result.project_path)
    run_flake8_in_generated_project(result.project_path)
    # run_precommit_in_generated_project(result.project_path)
