#!/bin/sh
wget=/usr/bin/wget
rpmbld=/usr/bin/rpmbuild
sshk=/usr/bin/ssh-keyscan
curl=/usr/bin/curl
WORKDIR="/home/builder/rpm"
VERSION="$1"
SPECURL="https://raw.githubusercontent.com/ranjithtam/specfile/main/grpcurl.spec"
GRPURL="https://github.com/fullstorydev/grpcurl/archive/refs/tags/v${VERSION}.tar.gz"
$wget ${SPECURL}
$wget ${GRPURL}
$rpmbld -ba --define "grpcurlver ${VERSION}" /home/builder/rpm/grpcurl.spec
echo >> ~/.ssh/known_hosts
$sshk us201 >> ~/.ssh/known_hosts
cd /home/builder/rpm/x86_64 && $curl --insecure -u ranjith:must0xLogan -T *.rpm sftp://us201/garage/ranjith/
