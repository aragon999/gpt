#!/usr/bin/env bash

set -eu

package_dir=/gpt-packages

if [ $# -eq 1 ]; then
    package="${1}"

    if [ -f "${package_dir}/$package" ]; then
        # TODO: remove old image
        # TODO: maybe unzip files, if downloaded from github
        echo "Installing ${package_dir}/$package"
        dpkg -i "${package_dir}/$package"
        exit
    else
        echo "Package ${package_dir}/$package not found"
        exit
    fi

fi

available_packages=$(find "${package_dir}" -type f -exec basename {} \;)

echo "Available packages:"
for package in ${available_packages}; do
    echo "  ${package}"
done
