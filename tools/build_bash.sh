#!/usr/bin/env bash
# This script is used to build a customized Git Bash for windows pacakge that only include bash and no other unnecessary files

# Get script directory
DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd $DIR/../dist

# Get the git distribution if it doesn't exist
if [ ! -f git.tar.bz2 ]; then
  # NOTE: Git for Windows v2.44 is the last release to support Windows 7 and 8
  URL="https://github.com/git-for-windows/git/releases/download/v2.44.0.windows.1/Git-2.44.0-32-bit.tar.bz2"
  wget $URL -O git.tar.bz2
fi

# Unzip the git distribution to git directory
# Ignore the unnecessary files
rm -rf git
mkdir git
tar -xvf git.tar.bz2 -C git --exclude-from="$DIR/bash_ignore.txt"