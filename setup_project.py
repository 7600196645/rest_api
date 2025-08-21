#2)2) Write a Python script to set up a Django project and install packages like django, djangorestframework, requests, etc
import os
import subprocess
import sys

def run_command(command):
    print(f"\n>>> Running: {command}")
    subprocess.run(command, shell=True, check=True)

def main():
    project_name = "myproject"
    venv_name = "myenv"

    # 1. Create project directory
    os.makedirs(project_name, exist_ok=True)
    os.chdir(project_name)

    # 2. Create virtual environment
    run_command(f"python -m venv {venv_name}")

    # 3. Show activation command
    activate_cmd = f"{venv_name}\\Scripts\\activate" if os.name == 'nt' else f"source {venv_name}/bin/activate"
    print(f"\n>>> To activate your virtual environment, run:\n{activate_cmd}\n")

    # 4. Install required packages
    pip_cmd = f"{venv_name}\\Scripts\\pip" if os.name == 'nt' else f"{venv_name}/bin/pip"
    run_command(f"{pip_cmd} install django djangorestframework requests")

    print("\n✅ Environment setup complete. Now you can run:")
    print(f"{activate_cmd}")
    print("django-admin startproject myproject .")
    print("python manage.py startapp myapp")

if __name__ == "__main__":
    main()

