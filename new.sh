apt-get install vim bash-completion ssh
iptables -A INPUT -p all -d 192.168.31.19 -j ACCEPT
iptables -P INPUT DROP
iptables -A INPUT -i lo -p all -j ACCEPT
iptables -t nat -A PREROUTING -p tcp -d 192.168.31.19 --dport 52100:52199 -j DNAT --to-destination 192.168.31.20
iptables -t nat -A PREROUTING -p tcp -d 192.168.31.19 --dport 52200:52300 -j DNAT --to-destination 192.168.31.21
iptables -t nat -A POSTROUTING -p all -j MASQUERADE
touch /root/iptables.conf
iptables-save > /root/iptables.conf
