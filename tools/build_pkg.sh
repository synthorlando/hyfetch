#!/usr/bin/env bash

# Get script directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR/..

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

# Build bash pacakge
$DIR/build_bash.sh

# Unzip the wheel
unzip $file -d wheel

# Copy the git distribution to the wheel
cp -r git/ wheel/hyfetch/

# Change the file name (replace -none-any with -win_amd64)
new_name="$(echo $file | sed 's/-none-any/-win32/')"

# Zip the wheel to win_amd64.whl
cd wheel && zip -y -r "../$new_name" * && cd ..

# Check again
twine check $new_name