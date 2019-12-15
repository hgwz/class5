#!/bin/bash

RED='\e[1;91m'
GREEN='\e[1;92m'
WHITE='\e[1;97m'
NC='\e[0m'

LOCAL_IP=""
SERVER_RMI_PORT="6000"
SERVER_PORT="1299"

get_system_ip()
{
	LOCAL_IP=$(ifconfig eth0 | grep 'inet ' | awk '{print $2}' | awk -F ':' '{print $2}')
	echo $LOCAL_IP

}

start()
{	
	FLAG=$(ps -ef | grep 'jmeter-server' | grep -v 'grep' | wc -l)
	if [ $FLAG -eq 0 ];then
		echo "Start jmeter server!"
		get_system_ip
		LOCAL_IP="192.168.31.154"
		echo /tmp/apache-jmeter-5.1/bin/jmeter-server -Djava.rmi.server.hostname=$LOCAL_IP -Dserver.rmi.localport=$SERVER_RMI_PORT -Dserver_port=$SERVER_PORT&
		/tmp/apache-jmeter-5.1/bin/jmeter-server -Djava.rmi.server.hostname=$LOCAL_IP -Dserver.rmi.localport=$SERVER_RMI_PORT -Dserver_port=$SERVER_PORT &
		echo -e $GREEN"Start jmeter server successed!"$NC
	else
		echo -e $RED"Jmeter server is already start!"$NC
	fi
}

stop()
{	
	FLAG=$(ps -ef | grep 'jmeter-server' | grep -v 'grep' | wc -l)
	if [ $FLAG -eq 0 ];then
		echo -e $RED"Jmeter server not starte!"$NC
	else
		echo "Stop jmeter server!"
		kill -9 $(ps -ef | grep 'jmeter' | grep -v grep | awk '{print $2}') && echo -e $GREEN"Stop jmeter server successed!"$NC
	fi
}

restart()
{
	FLAG=$(ps -ef | grep 'jmeter-server' | grep -v 'grep' | wc -l)
	if [ $FLAG -eq 0 ];then
		start
	else
		stop
		sleep 2
		start
	fi
}

case $1 in
	'start')
		start;;
	'stop')
		stop;;
	'restart')
		restart;;
	*)
		echo "Usage: $0 {start|stop|restart}"
		exit 1
esac