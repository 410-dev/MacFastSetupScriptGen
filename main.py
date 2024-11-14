import os
import requests
from bs4 import BeautifulSoup
import subprocess
import base64
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Manual mapping for applications with different Homebrew cask names
MANUAL_MAPPING = {
    "iTerm.app": "iterm2",
    "Chromium.app": "eloston-chromium"
}

# Blacklist for applications that should not be processed
BLACKLIST = [
    "SomeBlacklistedApp.app",
]

def get_application_names():
    app_dirs = ["/Applications", os.path.expanduser("~/Applications")]
    app_names = []

    for app_dir in app_dirs:
        if os.path.exists(app_dir):
            for file_name in os.listdir(app_dir):
                if file_name.endswith(".app") and file_name not in BLACKLIST:
                    app_names.append(file_name)

    # Process names: lowercase, replace spaces with dashes, remove .app extension
    processed_names = [
        MANUAL_MAPPING.get(app, app.lower().replace(" ", "-").replace(".app", ""))
        for app in app_names
    ]

    return sorted(processed_names)

def check_homebrew_casks(app_names):
    found_apps = []
    not_found_apps = []

    for i, app_name in enumerate(app_names, start=1):
        print(f"[{i}/{len(app_names)}] Checking {app_name} formulae...", end='')
        url = f"https://formulae.brew.sh/cask/{app_name}#default"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            name_tag = soup.find("p", class_="names")
            desc_tag = soup.find("p", class_="desc")

            if name_tag and desc_tag:
                found_apps.append(app_name)
                print(" Found")
            else:
                not_found_apps.append(app_name)
                print(" Not found")
        else:
            not_found_apps.append(app_name)
            print(" Not found")

    return found_apps, not_found_apps

def get_homebrew_packages():
    result = subprocess.run(["brew", "list"], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error: Unable to list Homebrew packages.")
        return []
    
    packages = result.stdout.splitlines()
    selected_packages = []
    i = 0

    print("Homebrew packages:")
    for package in packages:
    	print(f" - {package}")

    while i < len(packages):
        package = packages[i]
        user_input = input(f"[{i + 1}/{len(packages)}] Include package '{package}'? (y/n/b [back]/aa [all]/nn [none]): ")
        if user_input.lower() == 'y':
            if package not in selected_packages:
                selected_packages.append(package)
            i += 1
        elif user_input.lower() == 'n':
            if package in selected_packages:
                selected_packages.remove(package)
            i += 1
        elif user_input.lower() == 'b' and i > 0:
            i -= 1
        elif user_input.lower() == 'aa':
            selected_packages.extend([pkg for pkg in packages if pkg not in selected_packages])
            break
        elif user_input.lower() == 'nn':
            break
        else:
            print("Invalid input. Please enter 'y', 'n', 'b', 'aa', or 'nn'.")

    return selected_packages

def get_homebrew_cask_packages(found_apps):
    selected_cask_apps = []
    i = 0

    while i < len(found_apps):
        app = found_apps[i]
        user_input = input(f"[{i + 1}/{len(found_apps)}] Include cask package '{app}'? (y/n/b [back]/aa [all]/nn [none]): ")
        if user_input.lower() == 'y':
            if app not in selected_cask_apps:
                selected_cask_apps.append(app)
            i += 1
        elif user_input.lower() == 'n':
            if app in selected_cask_apps:
                selected_cask_apps.remove(app)
            i += 1
        elif user_input.lower() == 'b' and i > 0:
            i -= 1
        elif user_input.lower() == 'aa':
            selected_cask_apps.extend([a for a in found_apps if a not in selected_cask_apps])
            break
        elif user_input.lower() == 'nn':
            break
        else:
            print("Invalid input. Please enter 'y', 'n', 'b', 'aa', or 'nn'.")

    return selected_cask_apps

def clone_shell_config_files():
    shell_files = [".zshrc", ".zprofile", ".bashrc", ".bash_profile"]
    cloned_content = {}
    file_operations = {}

    for shell_file in shell_files:
        file_path = os.path.expanduser(f"~/{shell_file}")
        if os.path.exists(file_path):
            user_input = input(f"Do you want to clone the contents of '{shell_file}'? (y/n): ")
            if user_input.lower() == 'y':
                while True:
                    operation = input(f"How do you want to handle '{shell_file}'? (o [overwrite]/a [append]/p [prepend]): ")
                    if operation.lower() in ['o', 'a', 'p']:
                        with open(file_path, "r") as f:
                            content = f.read()
                        cloned_content[shell_file] = content
                        file_operations[shell_file] = {'o': 'overwrite', 'a': 'append', 'p': 'prepend'}[operation.lower()]
                        break
                    else:
                        print("Invalid input. Please enter 'o', 'a', or 'p'.")

    return cloned_content, file_operations

def add_post_run_script():
    user_input = input("\nDo you want to add a post run script? (y/n): ")
    post_run_script = []

    if user_input.lower() == 'y':
        print("Enter your post run script line by line. Type 'end' to finish.")
        while True:
            line = input()
            if line.lower() == 'end':
                break
            post_run_script.append(line)

    return post_run_script

def generate_bash_script():
    app_names = get_application_names()
    found_apps, not_found_apps = check_homebrew_casks(app_names)

    print("\nApplications found in Homebrew casks:")
    for app in found_apps:
        print(f"- {app}")

    print("\nApplications not found in Homebrew casks:")
    for app in not_found_apps:
        print(f"- {app}")

    selected_cask_apps = get_homebrew_cask_packages(found_apps)
    print(f"\nSelected {len(selected_cask_apps)} Homebrew cask packages: ")
    for app in selected_cask_apps:
        print(f"{app}", end=" ")
    print("\n")


    selected_packages = get_homebrew_packages()
    print(f"\nSelected {len(selected_packages)} Homebrew packages: ")
    for package in selected_packages:
        print(f"{package}", end=" ")
    print("\n")

    cloned_files, file_operations = clone_shell_config_files()
    if cloned_files:
        print("\nCloned shell configuration files:")
        for file_name, content in cloned_files.items():
            operation = file_operations[file_name]
            length = len(content.split("\n"))
            print(f"Handling '{file_name}' with operation '{operation}':\n{length}\n")
    
    post_run_script = add_post_run_script()
    if post_run_script:
        length = len(post_run_script)
        print(f"\nTotal {length} lines of post run script setup.")
        
    print()

    refresh = ""
    while refresh not in ["y", "n"]:
        refresh = input(f"Do you want the script to refresh the Dock and Finder after script is done? (y/n) ")
        refresh = refresh.lower()
    
    # Compile the bash script
    bash_script = """#!/bin/bash

# Step 1: Install Homebrew
echo "[1/5] Installing Homebrew..."
/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"
eval "$(/opt/homebrew/bin/brew shellenv)"

# Step 2: Install Homebrew non-cask packages
echo "[2/5] Installing Homebrew non-cask packages..."
brew install """ + " ".join(selected_packages) + "\n"

    bash_script += "\n# Step 3: Install Homebrew cask packages\necho \"[3/5] Installing Homebrew cask packages...\"\n"
    bash_script += "brew install --cask " + " ".join(found_apps) + "\n"

    # Step 4: Handle shell configuration files
    bash_script += "\n# Step 4: Update shell configuration files\n"
    for file_name, content in cloned_files.items():
        operation = file_operations[file_name]
        file_path = f"~/{file_name}"
        encoded_content = base64.b64encode(content.encode()).decode()
        if operation == 'overwrite':
            bash_script += f"echo '[4/5] Overwriting {file_path}...'\necho {encoded_content} | base64 --decode > {file_path}\n"
        elif operation == 'append':
            bash_script += f"echo '[4/5] Appending to {file_path}...'\necho {encoded_content} | base64 --decode >> {file_path}\n"
        elif operation == 'prepend':
            bash_script += f"echo '[4/5] Prepending to {file_path}...'\necho {encoded_content} | base64 --decode | cat - {file_path} > temp && mv temp {file_path}\n"

    # Step 5: Add post run script
    length = len(post_run_script)
    bash_script += f"\n# Step 5: Execute post run script\necho \"[5/5] Executing {length} lines of post run script...\"\n"
    if post_run_script:
        for line in post_run_script:
            bash_script += f"{line}\n"

    if refresh == "y":
        bash_script += f"killall Dock Finder\n"

    # Complete configuration message
    bash_script += "\necho 'Configuration complete.'"

    # Save the compiled bash script to a file
    script_path = "initial_setup_compiled.sh"
    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)
    print(f"Bash script '{script_path}' has been created and made executable.")


if __name__ == "__main__":
    generate_bash_script()
