<p align=“center”>
<img src="https://i.postimg.cc/wBCTvXtJ/Ethereum-Update-Moves-On-To-Goelri-And-Sepolia-Testnets-After-A-Successful-Merge-On-Ropsten.png"width="900"/></a>
</p>

# In this guide we will setup ETH RPC Archive node on Sepolia network

#### Flollowing parametrs:

- 4-CPU
- 8-GBRAM
- 250-GBSSD 

## 1. Node Preparation
```
sudo apt update && sudo apt upgrade -y
```
```
sudo apt install make clang pkg-config libssl-dev libclang-dev build-essential git curl ntp jq llvm cmake -y
```
```
sudo apt -y install software-properties-common wget curl ccze
```

## 2. Generate secret key for JWT based authentication
```
mkdir database && mkdir database/geth $$ mkdir database/lighthouse
```
```
sudo openssl rand -hex 32 | tr -d "\n" > "/root/database/jwtsecret"
```

## 3. Installing Geth
```
sudo add-apt-repository -y ppa:ethereum/ethereum
```
```
sudo apt -y install geth
```
## 4. Install Lighthouse
```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```
```
source "$HOME/.cargo/env"
```
```
cd ~
git clone -b unstable https://github.com/sigp/lighthouse.git
```
```
cd lighthouse && make
```

## 4. Configuring and launch Geth and Lightnode node.
```
sudo tee /etc/systemd/system/geth.service > /dev/null <<EOF
[Unit]
Description=Archive Sepolia Geth Node
Wants=network-online.target
After=network-online.target
[Service]
User=$USER
Restart=on-failure
RestartSec=15
Type=simple
LimitNOFILE=65535
ExecStart=/usr/bin/geth --sepolia --syncmode full --gcmode archive --port 30333 --cache 4096 --rpc.txfeecap 2 --http --http.api net,eth,personal,web3,engine,admin,debug --authrpc.vhosts=localhost --authrpc.port 8561 --http.addr 0.0.0.0 --http.port 8545 --http.vhosts * --http.corsdomain * --ws --ws.addr 0.0.0.0 --ws.port 8546 --ws.api net,eth,personal,web3,engine,admin,debug,trace --ws.origins * --datadir /root/database/geth --authrpc.jwtsecret=/root/database/jwtsecret

[Install]
WantedBy=multi-user.target
EOF
```
Launch our Geth node
```
sudo systemctl daemon-reload
sudo systemctl enable geth
sudo systemctl start geth
sudo journalctl -u geth -f -n 100
```
Our node start looking for peers and beacon. Now we need configure our prysm beacon.
```
sudo tee /etc/systemd/system/lighthouse.service > /dev/null <<EOF
[Unit]
Description=Lighthouse Sepolia Node
Wants=network-online.target
After=network-online.target
[Service]
User=$USER
Restart=on-failure
RestartSec=15
Type=simple
LimitNOFILE=65535
ExecStart=/root/.cargo/bin/lighthouse --network sepolia --debug-level info beacon_node --datadir /root/database/lighthouse --http --http-address 0.0.0.0 --metrics --execution-endpoints http://127.0.0.1:8561 --disable-deposit-contract-sync --enr-udp-port=7000 --enr-tcp-port=7000 --discovery-port=7000 --checkpoint-sync-url https://sepolia.checkpoint-sync.ethdevops.io --execution-jwt "/root/database/jwtsecret"

[Install]
WantedBy=multi-user.target
EOF
```
Launch our Lighthouse node
```
sudo systemctl daemon-reload
sudo systemctl enable lighthouse
sudo systemctl start lighthouse
sudo journalctl -u lighthouse -f -n 100
```
By command bellow you can check a status of synchronization process of your node.
```
curl -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  --data '{"jsonrpc":"2.0","method":"eth_syncing","params":[],"id":1}'
```
- If the show `false` that means that your node is fully synchronized.
#
