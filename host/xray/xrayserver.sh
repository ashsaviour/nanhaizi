# follow https://cscot.pages.dev/2023/03/02/Xray-REALITY-tutorial/
apt update && apt upgrade

echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf
echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf
sysctl -p

bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install --beta -u root

xray uuid
# 2925cde2-e07d-4edb-b6d4-93de9ed830ff
xray x25519
# Private key: uMC8FdTUQxlyUE8WZbI1YmRq4ZuFYdzdbc2IkC60GBY
# Public key: r89W6lLyf1TJC786NST78eOW4644TEXHssxxC4IIPBA
# shortId: b3
# camouflage site: www.microsoft.com

vim /usr/local/etc/xray/config.json

systemctl restart xray
