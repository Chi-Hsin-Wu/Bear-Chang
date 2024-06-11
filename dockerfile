FROM ubuntu:22.04

RUN apt-get update -y && \
apt-get install -y software-properties-common

RUN apt-get update -y --allow-unauthenticated && \
	apt-get install -y cmake \
	git \
	libtool-bin \
	libmbedtls-dev \
	libboost-program-options-dev \
	libconfig++-dev \
	libsctp-dev \
	g++ \
	iputils-ping \
	vim \
        tmux \
	autoconf  \
	automake \
	net-tools \
        libnetfilter-queue-dev \
        python3-pip \
        iptables

# update pip3
RUN pip3 install -U pip

# netfilterqueue & scapy
RUN python3 -m pip install netfilterqueue scapy
# pycrate & CryptoMobile
RUN python3 -m pip install git+https://github.com/P1sec/pycrate git+https://github.com/P1sec/CryptoMobile

WORKDIR /root
