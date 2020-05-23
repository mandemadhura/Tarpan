RPMBUILD_PACKAGE="/usr/bin/rpmbuild"
RPMBUILD_DIR="/root/rpmbuild"
RPMBUILD_SOURCE_DIR="/root/rpmbuild/SOURCES"
PWD=$(pwd)
NAME="tarpan"
VERSION="0.0"
TMP_DIR="dist/tmp"

sudo /usr/bin/mkdir -p ${TMP_DIR}
sudo /usr/bin/tar -cf ${TMP_DIR}/${NAME}-${VERSION}.tgz ${PWD}/..
sudo /usr/bin/cp ${TMP_DIR}/${NAME}-${VERSION}.tgz ${RPMBUILD_SOURCE_DIR}

sudo ${RPMBUILD_PACKAGE} -ba ${PWD}/${NAME}.spec

sudo /usr/bin/rm -rf ${TMP_DIR}
sudo /usr/bin/rm -rf ${RPMBUILD_SOURCE_DIR}/${NAME}-${VERSION}.tgz


