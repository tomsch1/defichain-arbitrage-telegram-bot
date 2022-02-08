#/bin/bash


host=$1

user="ubuntu"
root_dir="/home/ubuntu"
application_dir="$root_dir/defichain-arbitrage-telegram-bot"


ssh $user@$host "mkdir $application_dir"

echo "Deploying application"
scp -r ../*.py ../requirements.txt $user@$host:$application_dir


echo "Deploying config and user data"
scp -r ../application.properties ../crypto_alarms.json ../stock_alarms.json $user@$host:$application_dir

echo "Installing dependencies"
ssh $user@$host "sudo apt update; sudo apt install -y python3 python3-pip"


echo "Installing dependencies from requirements.txt"
ssh $user@$host pip3 install -r $application_dir/requirements.txt

echo "Installing systemD service"
systemd_name="defichain-arbitrage-telegram-bot.service"
scp ./$systemd_name $user@$host:$root_dir
ssh $user@$host "sudo cp $root_dir/$systemd_name /etc/systemd/system/; sudo systemctl daemon-reload; sudo systemctl enable $systemd_name; sudo systemctl restart $systemd_name; rm $root_dir/$systemd_name"


