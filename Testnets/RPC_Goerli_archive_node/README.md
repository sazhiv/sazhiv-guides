<p align=“center”>
<img src="https://i0.wp.com/www.portalkripto.com/wp-content/uploads/2023/02/ilustrasi-berita-2023-02-27T105243.210.png?resize=1024%2C576&ssl=1"width="600"/></a>
</p>

# In this guide we will setup ETH RPC Archive node on Goerli network

#### Flollowing parametrs:

- 4-CPU
- 8-GBRAM
- 500+-GBSSD 

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
mkdir database && mkdir database/erigon $$ mkdir database/lighthouse
```
```
sudo openssl rand -hex 32 | tr -d "\n" > "/root/database/jwtsecret"
```

## 3. Install Erigon
```
git clone --branch stable --single-branch https://github.com/ledgerwatch/erigon.git
```
```
cd erigon && make
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

## 5. Configuring and launch Erigon and Lighthouse node.
```
sudo tee /etc/systemd/system/erigon.service > /dev/null <<EOF
[Unit]
Description=Archive Goerli Erigon Node
Wants=network-online.target
After=network-online.target
[Service]
User=$USER
Restart=always
RestartSec=15
Type=simple
LimitNOFILE=65535
ExecStart=/root/erigon/build/bin/erigon --externalcl --chain=goerli --datadir /root/database/erigon --p2p.protocol 66 --p2p.allowed-ports 30309 --port 30309 --http.vhosts '*' --http.port 8545 --http.addr 0.0.0.0 --http.corsdomain '*' --http.api 'eth,erigon,net,web3,trace,txpool,debug' --ws --private.api.addr=0.0.0.0:9099 --metrics --metrics.port 6066 --metrics.addr 0.0.0.0 --authrpc.jwtsecret="/root/database/jwtsecret"

[Install]
WantedBy=multi-user.target
EOF
```
Launch our Erigon node
```
sudo systemctl daemon-reload
sudo systemctl enable erigon
sudo systemctl start erigon
sudo journalctl -u erigon -f -n 100
```
Our node start looking for peers and beacon. Now we need configure our lighthouse beacon.
```
sudo tee /etc/systemd/system/lighthouse.service > /dev/null <<EOF
[Unit]
Description=Lighthouse Goerli Node
Wants=network-online.target
After=network-online.target
[Service]
User=$USER
Restart=on-failure
RestartSec=15
Type=simple
LimitNOFILE=65535
ExecStart=/root/.cargo/bin/lighthouse --network goerli --debug-level info beacon_node --datadir /root/database/lighthouse --eth1 --http --http-allow-sync-stalled --metrics --merge --execution-endpoints http://127.0.0.1:8551 --enr-udp-port=9000 --enr-tcp-port=9000 --discovery-port=9000 --checkpoint-sync-url=https://goerli.checkpoint-sync.ethpandaops.io --jwt-secrets="/root/database/jwtsecret"

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
## 6. RPC urls:
- `http://YOUR_IP:8545`
- `ws://YOUR_IP:8545`
