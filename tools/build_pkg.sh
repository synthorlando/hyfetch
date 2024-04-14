#!/usr/bin/env bash

set -e

# Remove the old build
rm -rf dist/
rm -rf build/

# Remove git from the source code before building
rm -rf hyfetch/git/

# Build python from setup.py
python3 setup.py sdist bdist_wheel

# Check
twine check dist/*

# =================
# Build for windows
cd dist

# Get the file name
file=$(ls | grep .whl)

# Get the git distribution if it doesn't exist
if [ ! -f git.tar.bz2 ]; then
  #URL="https://github.com/git-for-windows/git/releases/download/v2.44.0.windows.1/Git-2.44.0-64-bit.tar.bz2"
  # NOTE: Git for Windows v2.44 is the last release to support Windows 7 and 8
  URL="https://github.com/git-for-windows/git/releases/download/v2.44.0.windows.1/Git-2.44.0-32-bit.tar.bz2"
  wget $URL -O git.tar.bz2
fi

# Unzip the git distribution to git directory
mkdir git
tar -xvf git.tar.bz2 -C git

# Unzip the wheel
unzip $file -d wheel

# Copy the git distribution to the wheel
cp -r git/ wheel/hyfetch/

# Change the file name (replace -none-any with -win_amd64)
new_name="$(echo $file | sed 's/-none-any/-win32/')"

# Zip the wheel to win_amd64.whl
cd wheel && zip -r "../$new_name" * && cd ..

# Check again
twine check $new_name