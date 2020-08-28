#!/usr/bin/env bash

set -eu

MAKE_BUILD_FLAGS="${@:2}"

code_dir=/gpt-code

cd ${code_dir}

./bootstrap.sh

mkdir -p build
cd build
../configure || cat config.log
make ${MAKE_BUILD_FLAGS}
