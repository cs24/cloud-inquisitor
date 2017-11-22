#!/bin/bash -e
set -o nounset
# Intended to create a standard dev & build environment with code mounted from the host.
# Gulp is watching for minor front-end code changes.

# TODO: start task scheduler
# TODO: don't overwrite certs and keys

# BACKEND
cd ${APP_BACKEND_BASE_PATH}
mkdir -p ./logs
rm -rf ./cinq.egg-info ./.eggs
pip3 install --upgrade -r requirements.txt
pip3 install --no-deps -e .

SECRET_KEY=$(openssl rand -hex 32)
sed -e "s|APP_DEBUG|${APP_DEBUG}|" \
    -e "s|APP_DB_URI|${APP_DB_URI}|" \
    -e "s|APP_SECRET_KEY|${SECRET_KEY}|" \
    -e "s|APP_USE_KMS|${APP_USE_KMS}|" \
    -e "s|APP_USER_DATA_URL|${APP_USER_DATA_URL}|" \
    -e "s|APP_AWS_API_ACCESS_KEY|${APP_AWS_API_ACCESS_KEY}|" \
    -e "s|APP_AWS_API_SECRET_KEY|${APP_AWS_API_SECRET_KEY}|" \
    /workspace/packer/files/backend-settings.py > ${APP_BACKEND_BASE_PATH}/settings/production.py
export CINQ_SETTINGS=${APP_BACKEND_BASE_PATH}/settings/production.py

# A module used by manage.py expects private.key to be present, even if not needed
openssl genrsa -out ${APP_BACKEND_BASE_PATH}/settings/ssl/private.key 2048

sudo mysql -u root -e "create database cinq; grant ALL on cinq.* to 'cinq'@'localhost' identified by 'changeme';" || true
sudo -u www-data -E python3 manage.py db upgrade

sudo -u www-data -E python3 manage.py setup --headless
kill `pidof python3` >/dev/null 2>&1 || true
nohup sudo -u www-data -E python3 manage.py runserver &
sleep 5
password_line=$(grep -oE "password:.+$" logs/apiserver.log* | head -1)

# FRONTEND
cd ${APP_FRONTEND_BASE_PATH}
# kill any gulp so we can move node_modules
kill `pidof gulp` >/dev/null 2>&1 || true
# optimization - move and delete in background
mv node_modules node_modules.old >/dev/null 2>&1 && nohup time rm -rf ./node_modules.old >rm.log 2>&1 &
# TODO: change script to be running as unprivileged user (vagrant, or ubuntu or centos) and sudo when needed.
sudo -i -u vagrant bash -c "cd `pwd`; npm i --quiet"

echo "pre gulp"
cd ${APP_FRONTEND_BASE_PATH}
rm -rf ./dist
# explicitly redirect nohup output to file or vagrant steals it and causes termination problems
sudo -u vagrant bash -c "nohup ./node_modules/.bin/gulp dev >nohup.out 2>&1" &
echo "Waiting for initial gulp nohup output..."
sleep 30
cat nohup.out
echo "did gulp"

# localhost cert
CERTINFO="/C=US/ST=CA/O=Riot Games/localityName=Los Angeles/commonName=cinq/organizationalUnitName=Operations/emailAddress=someone@example.com"
openssl req -x509 -subj "$CERTINFO" -days 3650 -newkey rsa:2048 -keyout cinq-frontend.key -nodes -out cinq-frontend.crt
mv cinq-frontend.key cinq-frontend.crt ${APP_BACKEND_BASE_PATH}/settings/ssl/

# configure_supervisor omitted

# nginx
echo "nginx..."
sed -e "s|APP_FRONTEND_BASE_PATH|${APP_FRONTEND_BASE_PATH}/dist|g" \
    -e "s|APP_BACKEND_BASE_PATH|${APP_BACKEND_BASE_PATH}|g" \
        /workspace/packer/files/nginx-ssl.conf > /etc/nginx/sites-available/cinq.conf
ln -sfn /etc/nginx/sites-available/cinq.conf /etc/nginx/sites-enabled/cinq.conf
rm -f /etc/nginx/sites-enabled/default
service nginx restart

echo ""
echo "Cloud Inquisitor should be running at https://localhost"
echo "Admin password is probably ${password_line}"
echo "Watch gulp with: tail -f ../frontend/nohup.out"
echo "Run task scheduler by logging in via ssh (e.g. vagrant ssh), and then: python3 manage.py run_scheduler"
echo "Run end-to-end tests by being in directory with Vagrantfile, " \
     "and then: vagrant ssh -c \"cd /workspace/frontend/tests; bash ./test-e2e.sh\" "
