#!/bin/bash -e
# Intended to mimick production installation process and scripts.

mkdir -p ${APP_TEMP_BASE}
# Using /. to include hidden files like .js* for npm
cp -a /workspace/backend/. ${APP_TEMP_BASE}/cinq-backend
cp -a /workspace/frontend/. ${APP_TEMP_BASE}/cinq-frontend
cp -a /workspace/packer/files/. ${APP_TEMP_BASE}/files
cp -a /workspace/packer/scripts/install.sh ${APP_TEMP_BASE}/

cd ${APP_TEMP_BASE}
./install.sh

# Database setup
# Okay to error when DB already exists.
echo "Database setup..."
sudo mysql -u root -e "create database cinq; grant ALL on cinq* to 'cinq'@'localhost' identified by 'changeme';" || true

export CINQ_SETTINGS=/opt/cinq-backend/settings/production.py
cd /opt/cinq-backend
sudo -u www-data -E python3 manage.py db upgrade
echo ""
echo "Ignore line above about 'Failed loading configuration from database.' It was buffered before creating DB"
# Setup DB with default config according to setup
sudo -u www-data -E python3 manage.py setup --headless

systemctl restart supervisor.service

echo ""
echo "Default server should be running at https://localhost/ "
echo "Admin password is probably: $(grep -oE "password:.+$" logs/apiserver.log* | head -1)"
echo ""
echo "MANUAL STEP 0: SSH into vagrant@localhost port 2222 using vagrant/vagrant. Or $ vagrant ssh"
if [[ -z ${APP_AWS_API_SECRET_KEY} ]]; then
  echo "MANUAL STEP K: AWS key not present."
  echo "MANUAL STEP K: Insert AWS key:              $ sudo vi /opt/cinq-backend/settings/production.py"
fi
echo ""
echo "MANUAL STEP 0: What is running?             $ sudo supervisorctl status"
echo "MANUAL STEP 1: Required environment         $ export CINQ_SETTINGS=/opt/cinq-backend/settings/production.py"
echo "MANUAL STEP 2: start dev server:            $ sudo -u www-data -E python3 manage.py runserver"
echo "MANUAL STEP 3: start task scheduled:        $ sudo -u www-data -E python3 manage.py run_scheduler"
