#! /bin/bash

set -e
set -u

if [ ! -d "/home/pi/pi2fa" ]; then
  echo "Creating pi2fa directory"
  mkdir /home/pi/pi2fa
fi

cd /home/pi

sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt autoremove -y

sudo apt-get install dialog -y
sudo apt-get install python3-venv -y

tar xvf /home/pi/pi2fa-2022.10.9.1.tar.gz

#Check for Raspberry Pi 3B/3B+ and abort if not found
python3 /home/pi/check_pi_version.py

#Check for Debian Bullseye and abort if not found
python3 /home/pi/check_os_version.py

if [ ! -f "/etc/logrotate.d/pjsip" ]; then
  echo "Adding logrotate script"
  sudo cp /home/pi/logrotate_sip.txt  /etc/logrotate.d/pjsip
fi

if [ ! -d "/home/pi/pi2fa/venv" ]; then
  echo "Creating virtual environment"
  python3 -m venv /home/pi/pi2fa/venv
fi

source  /home/pi/pi2fa/venv/bin/activate
pip3 install --upgrade pip
pip3 install wheel

pip3 install -r /home/pi/pi2fa_requirements.txt

pip3 install /home/pi/pi2fa-2022.10.9.1-py3-none-any.whl
python3 /home/pi/pi_create_venv_symlinks.py

mv /home/pi/_pjsua2.cpython-39-arm-linux-gnueabihf.so /home/pi/pi2fa/venv/lib/python3.9/site-packages/_pjsua2.cpython-39-arm-linux-gnueabihf.so
mv /home/pi/pjsua2.py /home/pi/pi2fa/venv/lib/python3.9/site-packages/pjsua2.py
mv /home/pi/pi_run_pi2fa.sh /home/pi/pi2fa

chmod +x /home/pi/pi2fa/pi_run_pi2fa.sh

if [ ! -d "/home/pi/pi2fa/logs" ]; then
  echo "Creating logs folder"
  mkdir /home/pi/pi2fa/logs
fi

echo "Succesful Install, run /home/pi/pi_run_pi2fa.sh to start"
