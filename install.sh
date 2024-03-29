username="menuprog"
id "$username"
if [ $? -eq 0 ]
then
	echo "User already exists"
else
	echo "No such user"
	sudo useradd -s /bin/bash -m "$username"
	echo "New user $username is created"
fi
if [ `sudo grep "$username ALL=(ALL) NOPASSWD: ALL" /etc/sudoers | wc -l` -eq 0 ]
then
	echo  username=$username' ;echo "$username ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers' | sudo su
fi
echo 'test -d ~/.ssh' | sudo su $username
if [ $? -eq 1 ]
then
	echo 'mkdir ~/.ssh' | sudo su $username
fi

if [ `yum > /tmp/testing; echo $?` -eq 0 ]
then
	echo "sudo yum install espeak-ng python36 awscli -y;sudo pip3 install pyttsx3 boto boto3" | sudo su $username
elif [ `apt-get > /tmp/testing; echo $?` -eq 1 ]
then
	echo "sudo apt-get install espeak-ng python3 awscli -y;sudo pip3 install pyttsx3 boto boto3" | sudo su $username
else
	echo -e "\nInstall the following softwares manually:\n"
	echo -e "\t\tespeak-ng, python3, and awscli"
	echo -e "\nAlso install the following python packages\n"
	echo -e "\t\tpyttsx3 boto boto3"
fi
