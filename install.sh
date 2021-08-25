username="menuprog"
id "$username"
if [ $? -eq 0 ]
then
	echo "user exists"
	exit 1
else
	echo "no such user"
fi
sudo useradd -s /bin/bash -G sudo -m "$username"
sudo passwd $username
echo 'test -d ~/.ssh' | sudo su $username
if [ $? -eq 1 ]
then
	mkdir 
echo "pip3 install pyttsx3" 
