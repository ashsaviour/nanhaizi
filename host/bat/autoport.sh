# sudo -i
# crontab -e
# 15 22 * * * /home/ashsaviour20244/autoport.sh 

sudo apt -y install jq
config_path="/usr/local/etc/v2ray/config.json"
old_port=$( jq '.inbounds[0].port' "$config_path")
if [ $old_port -eq 37890 ]; then
    new_port=37881
else
    new_port=$((old_port+1))
fi
echo "new_port: $new_port"
jq ".inbounds[0].port = $new_port" "$config_path" > temp.json
sudo mv -f temp.json "$config_path"
sudo systemctl restart v2ray