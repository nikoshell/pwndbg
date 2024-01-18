# This dockerfile was created for development & testing purposes, for APT-based distro.
#
# Build as:             docker build -t pwndbg .
#
# For testing use:      docker run --rm -it --cap-add=SYS_PTRACE --security-opt seccomp=unconfined pwndbg bash
#
# For development, mount the directory so the host changes are reflected into container:
#   docker run -it --cap-add=SYS_PTRACE --security-opt seccomp=unconfined -v `pwd`:/pwndbg pwndbg bash
#

ARG image=mcr.microsoft.com/devcontainers/base:jammy
FROM $image

WORKDIR /pwndbg

ENV LANG en_US.utf8
ENV TZ=America/New_York
ENV ZIGPATH=/opt/zig
ENV PWNDBG_VENV_PATH=/venv

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    apt-get update && \
    apt-get install -y locales && \
    rm -rf /var/lib/apt/lists/* && \
    localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8 && \
    apt-get update && \
    apt-get install -y vim

ADD . /pwndbg/
RUN ./setup.sh
RUN ./setup-dev.sh
RUN pip install -r dev-requirements.txt
# RUN pipx install -f -r dev-requirements.txt

ARG LOW_PRIVILEGE_USER="vscode"

# RUN pwndbg
