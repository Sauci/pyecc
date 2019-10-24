FROM frolvlad/alpine-glibc:latest

ENV PROJECT_DIR=/usr/project
ENV TOOL_DIR=/usr/tools

# copy required elements.
COPY requirements.txt requirements.txt

# install packages for environment.
RUN apk add --no-cache --update \
    cmake \
    git \
    make \
    python3-dev

# install python requirements.
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

# install GNU ARM toolchain.
WORKDIR $TOOL_DIR
RUN wget -q https://developer.arm.com/-/media/Files/downloads/gnu-rm/8-2019q3/gcc-arm-none-eabi-8-2019-q3-update-linux.tar.bz2 && \
    tar xf gcc-arm-none-eabi-8-2019-q3-update-linux.tar.bz2 && \
    rm gcc-arm-none-eabi-8-2019-q3-update-linux.tar.bz2
ENV PATH="$TOOL_DIR/gcc-arm-none-eabi-8-2019-q3-update/bin:${PATH}"

# setup a shared volume.
WORKDIR $PROJECT_DIR
VOLUME ["$PROJECT_DIR"]
