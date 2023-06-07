
<p align="center">
 <img src="https://dev.optimism.io/content/images/size/w2000/2022/12/bedrock-BLUE.jpg"width="600"/></a>
</p>
### 0. Official sources.
[Node-operator-guide](https://community.optimism.io/docs/developers/bedrock/node-operator-guide)
[Configurations](https://community.optimism.io/docs/useful-tools/networks/#optimism-mainnet)
[Bedrock-Mission-Control](https://oplabs.notion.site/Bedrock-Mission-Control-EXTERNAL-fca344b1f799447cb1bcf3aae62157c5)

### 1. Update your server.
```
sudo apt update && sudo apt upgrade -y
```
```
sudo apt install make clang pkg-config libssl-dev libclang-dev build-essential git curl ntp jq llvm tmux unzip cmake wget liblz4-tool aria2 openssl -y
```
### 2. Install GO.
```
if ! [ -x "$(command -v go)" ]; then
  ver="1.19.7"
  cd $HOME
  sudo wget "https://golang.org/dl/go$ver.linux-amd64.tar.gz"
  sudo rm -rf /usr/local/go
  sudo tar -C /usr/local -xzf "go$ver.linux-amd64.tar.gz"
  sudo rm "go$ver.linux-amd64.tar.gz"
  sudo echo "export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin" >> ~/.bash_profile
  source ~/.bash_profile
fi
```
### 3. Create keys.
```
mkdir nodes && cd nodes
```
Create jwt_secret
```
openssl rand -hex 32 > $HOME/nodes/mainnet-op-geth/engine_jwt_secret.txt
sudo chmod 644 $HOME/nodes/mainnet-op-geth/engine_jwt_secret.txt
```
Create p2p node key
```
openssl rand -hex 32 > $HOME/nodes/mainnet-op-geth/p2pkey.txt
sudo chmod 644 $HOME/nodes/mainnet-op-geth/p2pkey.txt
```
### 4. Get Source code.
- [op-geth](https://github.com/ethereum-optimism/op-geth/releases) - see latest release
- [op-node](https://github.com/ethereum-optimism/optimism/releases) - see latest release
- Full Node Operators: The migrated (Bedrock) datadir required to spin up op-geth has been successfully hosted and is now ready for distribution: https://storage.googleapis.com/oplabs-mainnet-data/mainnet-bedrock.tar

### 5. Compiling the binary.
```
cd projects/op-geth
go build -o ~/go/bin/op-geth ./cmd/geth
```
```
cd projects/optimism
go build -o ~/go/bin/op-node ./op-node/cmd
```

### 6. Create services.
#### op-geth
```
sudo tee <<EOF >/dev/null /etc/systemd/system/op-geth.service
[Unit]
Description=op-geth optimism
After=network-online.target

[Service]
User=$USER
ExecStart=$HOME/go/bin/op-geth \
  --ws \
  --ws.port=8746 \
  --ws.addr=0.0.0.0 \
  --ws.origins="*" \
  --ws.api=eth,net,debug \
  --http \
  --http.port=8745 \
  --http.addr=0.0.0.0 \
  --http.vhosts="*" \
  --http.corsdomain="*" \
  --http.api=eth,net,debug \
  --authrpc.addr=localhost \
  --authrpc.jwtsecret=$HOME/nodes/mainnet-op-geth/engine_jwt_secret.txt
  --authrpc.port=8751 \
  --authrpc.vhosts="*" \
  --datadir=$HOME/nodes/mainnet-op-geth/gethdata \
  --verbosity=3 \
  --rollup.disabletxpoolgossip=true \
  --rollup.sequencerhttp=https://mainnet-sequencer.optimism.io \
  --nodiscover \
  --syncmode=full \
  --maxpeers=0 \
  --verbosity=4 \
  --metrics \
  --metrics.addr=0.0.0.0 \
  --metrics.port=6770 \
  --networkid=10 \
  --pprof \
  --pprof.addr=0.0.0.0 \
  --pprof.port=6760 \
  --snapshot=false
Restart=always
RestartSec=3
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
EOF
 
cat /etc/systemd/system/op-geth.service
sudo systemctl enable op-geth
```
#### op-node
```
sudo tee <<EOF >/dev/null /etc/systemd/system/op-node.service
[Unit]
Description=op-node optimism
After=network-online.target

[Service]
User=$USER
ExecStart=$HOME/go/bin/op-node \
  --l1=http://YOUR_L1_NODE \
  --l1.trustrpc \
  --l1.rpckind=erigon \ 
  --l2=http://127.0.0.1:8751 \
  --network=mainnet \
  --verifier.l1-confs=2 \
  --l1.epoch-poll-interval=2m \
  --rpc.enable-admin \
  --rpc.addr=0.0.0.0 \
  --rpc.port=8845 \
  --metrics.enabled \
  --metrics.addr=0.0.0.0 \
  --metrics.port=6870 \
  --l2.jwt-secret=$HOME/nodes/mainnet-op-geth/engine_jwt_secret.txt \
  --pprof.enabled \
  --pprof.addr=0.0.0.0 \
  --pprof.port=6860 \
  --p2p.priv.path=$HOME/nodes/mainnet-op-node/p2p_priv.txt \
  --p2p.peerstore.path=$HOME/nodes/mainnet-op-node/opnode_peerstore_db \
  --p2p.discovery.path=$HOME/nodes/mainnet-op-node/opnode_discovery_db \
  --p2p.listen.ip=0.0.0.0 \
  --p2p.listen.tcp=2020 \
  --p2p.listen.udp=2020 \
  --p2p.peers.lo=10 \
  --p2p.peers.hi=20 \
  --p2p.nat \
  --log.level=info \
  --log.format=logfmt
Restart=always
RestartSec=3
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
EOF
 
cat /etc/systemd/system/op-node.service
sudo systemctl enable op-node
```
##### Note. If you have L1 node erigon, parameter --l1.rpckind=erigon is mandatory, otherwise you can do without it.

### 7. Start all services.
```
sudo systemctl daemon-reload
sudo systemctl restart op-geth
sudo systemctl restart op-node
```
### 8. Check logs.
```
sudo journalctl -u op-geth.service -f -n 100
sudo journalctl -u op-node.service -f -n 100
```
