%define url https://github.com/mandemadhura/Tarpan

Name:	   tarpan
Version:   0.0
Release:	1%{?dist}
Summary:	Installs Tarpan Sender and Receiver
BuildArch: noarch
Group:	System Environment/Daemons
License:	MIT
URL:	${url}
Source0: %{name}-%{version}.tgz

# BuildRequires:
Requires: rabbitmq-server

%description
Installs Tarpan with sender and receiver

%clean
sym_link_sender="/usr/local/bin/sender"
sym_link_receiver="/usr/local/bin/receiver"

# Removes the symbolic link
[ -L ${sym_link_sender} ] && rm ${sym_link_sender}
[ -L ${sym_link_receiver} ] && rm ${sym_link_receiver}

# Reset the RabbitMQ Configuration
rabbitmqctl stop_app
rabbitmqctl reset

%prep
%setup -n Tarpan

%build
%global __python %{__python3}

%install

TARPAN_INSTALL_DIR=/opt/Tarpan
SENDER_DIR=./sender
RECEIVER_DIR=./receiver

mkdir -p ${RPM_BUILD_ROOT}/${TARPAN_INSTALL_DIR}/sender ${RPM_BUILD_ROOT}/${TARPAN_INSTALL_DIR}/receiver
cp ./__init__.py ${RPM_BUILD_ROOT}/${TARPAN_INSTALL_DIR}
cp -rp ${SENDER_DIR} ${RPM_BUILD_ROOT}/${TARPAN_INSTALL_DIR}
cp -rp ${RECEIVER_DIR}  ${RPM_BUILD_ROOT}/${TARPAN_INSTALL_DIR}

%post
BIN_INSTALL_PATH=/usr/local/bin

# Create the symbolic link for sender and receiver
ln -s /opt/Tarpan/sender/sender.py ${BIN_INSTALL_PATH}/sender
ln -s /opt/Tarpan/receiver/receiver.py ${BIN_INSTALL_PATH}/receiver

# Start the RabbitMQ server service
systemctl start rabbitmq-server

%files
/opt/Tarpan/__init__.py
/opt/Tarpan/sender/*
/opt/Tarpan/receiver/*

%changelog
* Sun May 24 2020 Madhura Mande <mandemadhura@gmail.com>
- First Version of Tarpan RPM Spec file

