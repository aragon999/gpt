FROM gpt/base

ENV TZ=Europe/Berlin

RUN \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
        clang-9 libmpfr-dev libgmp-dev libssl-dev zlib1g-dev libmpich-dev \
        libopenmpi-dev libfftw3-dev

VOLUME /gpt-package
VOLUME /gpt-code
