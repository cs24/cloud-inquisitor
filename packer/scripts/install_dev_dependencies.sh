#!/bin/bash -eu

export DEBIAN_FRONTEND=noninteractive
# default-jre java for selenium headless browser server used by Protractor to help with AngularJS tests.
# Consider replacing with a selenium docker container.
apt-get -y install mysql-server unzip default-jre

# xvfb for chromium-browser for use by selenium (75 MB download)
# libgconf-2-4 because chromediriver started to fail without details when launching selenium via protractor
# https://github.com/angular/protractor/issues/3760
apt-get -y install xvfb chromium-browser libgconf-2-4
nohup Xvfb -ac :99 -screen 0 1280x1024x16 > /tmp/nohup.xvfb &


packer_version=0.12.3
packer_url=https://releases.hashicorp.com/packer/${packer_version}/packer_${packer_version}_linux_amd64.zip
mkdir -p /opt/packer
cd /opt/packer
wget -q -N ${packer_url}
unzip -oq packer_${packer_version}_linux_amd64.zip
cd -

