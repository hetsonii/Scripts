#!H:\Softwares\Git\git-bash.exe
if [ "$1" == "" ]
then
echo "You forgot an IP address!"
echo "Syntax: ./ipsweep.sh 192.168.1"

else
for ip in `seq 1 254`; do
(ping -n 1 $1.$ip | grep "bytes=32" | cut -d " " -f 3 | tr -d ":") &

done
fi
