%define url https://github.com/mandemadhura/Tarpan

Name:	   server
Version:   0.0
Release:	1%{?dist}
Summary:	Installs server which accepts requests for messenger
BuildArch: noarch
Group:	System Environment/Daemons
License:	MIT
URL:	${url}
Source0: %{name}-%{version}.tgz

# BuildRequires:
# Requires:

%description
Installs Server with other supported modules for completing the requests

%prep
%setup -n Tarpan

%build
%global __python %{__python3}

%install

TARPAN_INSTALL_DIR=/opt/Tarpan
UTILITY_DIR=./utility
STORE_DIR=./store
SERVER_DIR=./server

mkdir -p ${RPM_BUILD_ROOT}/${TARPAN_INSTALL_DIR}/server ${RPM_BUILD_ROOT}/${TARPAN_INSTALL_DIR}/utility ${RPM_BUILD_ROOT}/${TARPAN_INSTALL_DIR}/store
cp -rp ${UTILITY_DIR} ${RPM_BUILD_ROOT}/${TARPAN_INSTALL_DIR}
cp -rp ${STORE_DIR}  ${RPM_BUILD_ROOT}/${TARPAN_INSTALL_DIR}
cp -rp ${SERVER_DIR}  ${RPM_BUILD_ROOT}/${TARPAN_INSTALL_DIR}

%post

%postun

%files
/opt/Tarpan/server/*
/opt/Tarpan/utility/*
/opt/Tarpan/store/*

%changelog
* Mon Jun 01 2020 Madhura Mande <mandemadhura@gmail.com>
- First Version of Tarpan server RPM Spec file

