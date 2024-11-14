# MacFastSetupScript Generator

## Overview

This Python program helps automate the creation of a bash script for setting up your system with Homebrew and related tools. The script performs the following steps:

1. **Install Homebrew**
2. **Install Homebrew Non-Cask Packages**
3. **Install Homebrew Cask Packages**
4. **Clone and Modify Shell Configuration Files** (e.g., `.zshrc`, `.bash_profile`)
5. **Execute Post-Run Custom Scripts**

The script also includes interactive elements, allowing users to customize which Homebrew packages, cask packages, and configuration changes they want to include in the setup process.

## Features

- **Interactive Package Selection**: The script allows you to interactively select which Homebrew and cask packages you want to include or exclude. Options include selecting individual packages, selecting all, or skipping all.
- **Manual Mappings**: Handles certain applications that have different names in Homebrew than their `.app` name.
- **Configuration Cloning**: Copies and optionally modifies existing shell configuration files (`.zshrc`, `.bashrc`, etc.) through options to overwrite, append, or prepend content.
- **Custom Post-Run Script**: Users can add lines of shell commands that will be executed at the end of the setup process.
- **Safe Handling of Special Characters**: The script encodes configuration file content in Base64, ensuring that special characters are handled safely when included in the bash script.


## Usage Instructions

1. **Run the Script**: Execute the Python script to start the interactive process:
   ```sh
   python3 script_name.py
   ```

2. **Follow the Prompts**:
   - The script will prompt you to select Homebrew packages, cask packages, and handle shell configuration files.
   - You can interactively include or exclude packages, modify configuration files, and add post-run commands.

3. **Generated Bash Script**: After completing the prompts, the script will generate a bash file called `initial_setup_compiled.sh`. This file will be executable and ready to run your system setup.

4. **Execute the Bash Script**:
   ```sh
   ./initial_setup_compiled.sh
   ```

## Example Output

The generated bash script will look like this:

```bash
#!/bin/bash

# Step 1: Install Homebrew
echo "[1/5] Installing Homebrew..."
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Step 2: Install Homebrew non-cask packages
echo "[2/5] Installing Homebrew non-cask packages..."
brew install package1 package2

# Step 3: Install Homebrew cask packages
echo "[3/5] Installing Homebrew cask packages..."
brew install --cask cask1 cask2

# Step 4: Update shell configuration files
echo "[4/5] Updating shell configuration files..."
echo "config_content" | base64 --decode > ~/.zshrc

# Step 5: Execute post run script
echo "[5/5] Executing post run script..."
custom_command

echo 'Configuration complete.'
```

## Notes

- **Dependencies**: The script requires Python packages such as `requests` and `BeautifulSoup4`. Install them using:
  ```sh
  pip install -r requirements
  ```

- **Homebrew**: Ensure Homebrew is installed before running this script. You can install it with:
  ```sh
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```


## How It Works

The program is organized into several main functions:

### 1. `get_application_names()`

- Scans the `/Applications` and `~/Applications` directories for installed `.app` files.
- Processes application names to lowercase, replace spaces with dashes, and remove the `.app` extension.
- Uses a manual mapping (`MANUAL_MAPPING`) for applications that have different Homebrew cask names.

### 2. `check_homebrew_casks(app_names)`

- Checks if each application is available as a Homebrew cask by making requests to `https://formulae.brew.sh`.
- Categorizes applications into `found_apps` and `not_found_apps` based on availability.

### 3. `get_homebrew_packages()`

- Lists installed Homebrew packages and allows the user to select which ones to include in the setup.
- Options include selecting individual packages (`y`/`n`), going back (`b`), selecting all (`aa`), or selecting none (`nn`).

### 4. `get_homebrew_cask_packages(found_apps)`

- Similar to `get_homebrew_packages()`, this function allows users to select cask packages interactively.

### 5. `clone_shell_config_files()`

- Interactively allows users to clone the contents of their shell configuration files (`.zshrc`, `.bashrc`, etc.).
- Users can choose to **overwrite**, **append**, or **prepend** the existing content.

### 6. `add_post_run_script()`

- Allows users to add custom shell commands to be executed after the setup is complete.
- The input ends when the user types `end`.

### 7. `generate_bash_script()`

- Compiles all the gathered information into a bash script.
- The script includes:
  - Installing Homebrew.
  - Installing selected non-cask and cask packages.
  - Updating shell configuration files with user-selected operations (overwrite, append, prepend).
  - Executing the user-provided post-run script.
  - Printing progress status for each step to ensure transparency during execution.

## License

This project is licensed under the MIT License.

## Contribution

Feel free to open issues or submit pull requests for improvements. Contributions are welcome!



Documentation written by ChatGPT.
