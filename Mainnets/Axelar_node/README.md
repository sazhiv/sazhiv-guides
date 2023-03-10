
<p align="center">
 <img src="https://moonbeam.network/wp-content/uploads/2021/05/Axelar-Logo-Update.png"width="600"/></a>
</p>

### 1. Update your server.
```
sudo apt update && sudo apt upgrade -y
```
```
sudo apt install make clang pkg-config libssl-dev libclang-dev build-essential git curl ntp jq llvm tmux unzip cmake wget liblz4-tool aria2 -y
```
### 2. Get Binaries.
Check the appropriate version for the network accordingly:
- [Mainnet](https://docs.axelar.dev/resources/mainnet)
- [Testnet](https://docs.axelar.dev/resources/testnet)
```
AXELARD_RELEASE=v0.32.2
TOFND_RELEASE=v0.10.1
```
verify correct versions
```
echo $AXELARD_RELEASE $TOFND_RELEASE
```
create a temp dir for binaries
```
cd $HOME
mkdir binaries && cd binaries
```
get axelard, tofnd binaries and rename
```
wget https://github.com/axelarnetwork/axelar-core/releases/download/$AXELARD_RELEASE/axelard-linux-amd64-$AXELARD_RELEASE
wget https://github.com/axelarnetwork/tofnd/releases/download/$TOFND_RELEASE/tofnd-linux-amd64-$TOFND_RELEASE
mv axelard-linux-amd64-$AXELARD_RELEASE axelard
mv tofnd-linux-amd64-$TOFND_RELEASE tofnd
```
make binaries executable
```
chmod +x *
```
move to usr bin
```
sudo mv * /usr/bin/
```
check versions
```
cd $HOME
axelard version
tofnd --version
```
### 3. Generate keys.
To create new keys
```
axelard keys add broadcaster
axelard keys add validator
tofnd -m create
```
To recover exsiting keys
```
axelard keys add broadcaster --recover
axelard keys add validator --recover
tofnd -m import
```
### 4. Set environment variables.
For Testnet:
```
echo export CHAIN_ID=axelar-testnet-lisbon-3 >> $HOME/.profile
```
For Mainnet:
```
echo export CHAIN_ID=axelar-dojo-1 >> $HOME/.profile
```
```
echo export MONIKER=PUT_YOUR_MONIKER_HERE >> $HOME/.profile
VALIDATOR_OPERATOR_ADDRESS=`axelard keys show validator --bech val --output json | jq -r .address`
BROADCASTER_ADDRESS=`axelard keys show broadcaster --output json | jq -r .address`
echo export VALIDATOR_OPERATOR_ADDRESS=$VALIDATOR_OPERATOR_ADDRESS >> $HOME/.profile
echo export BROADCASTER_ADDRESS=$BROADCASTER_ADDRESS >> $HOME/.profile
echo export KEYRING_PASSWORD=PUT_YOUR_KEYRING_PASSWORD_HERE >> $HOME/.profile
source $HOME/.profile
```
### 5. Configuration setup.
Initialize your Axelar node, fetch configuration, genesis, seeds.
For Testnet:
```
axelard init $MONIKER --chain-id $CHAIN_ID
wget https://raw.githubusercontent.com/axelarnetwork/axelarate-community/main/configuration/config.toml -O $HOME/.axelar/config/config.toml
wget https://raw.githubusercontent.com/axelarnetwork/axelarate-community/main/configuration/app.toml -O $HOME/.axelar/config/app.toml
wget https://raw.githubusercontent.com/axelarnetwork/axelarate-community/main/resources/testnet/genesis.json -O $HOME/.axelar/config/genesis.json
wget https://raw.githubusercontent.com/axelarnetwork/axelarate-community/main/resources/testnet/seeds.toml -O $HOME/.axelar/config/seeds.toml
sed -i.bak 's/external_address = ""/external_address = "'"$(curl -4 ifconfig.co)"':26656"/g' $HOME/.axelar/config/config.toml
```
For Mainnet:
```
axelard init $MONIKER --chain-id $CHAIN_ID
wget https://raw.githubusercontent.com/axelarnetwork/axelarate-community/main/configuration/config.toml -O $HOME/.axelar/config/config.toml
wget https://raw.githubusercontent.com/axelarnetwork/axelarate-community/main/configuration/app.toml -O $HOME/.axelar/config/app.toml
wget https://axelar-mainnet.s3.us-east-2.amazonaws.com/genesis.json -O $HOME/.axelar/config/genesis.json
wget https://raw.githubusercontent.com/axelarnetwork/axelarate-community/main/resources/mainnet/seeds.toml -O $HOME/.axelar/config/seeds.toml
sed -i.bak 's/external_address = ""/external_address = "'"$(curl -4 ifconfig.co)"':26656"/g' $HOME/.axelar/config/config.toml
```
### 6. Sync From Snapshot.
```
axelard tendermint unsafe-reset-all
```
For Testnet:
```
URL=`curl -L https://quicksync.io/axelar.json | jq -r '.[] |select(.file=="axelartestnet-lisbon-3-pruned")|.url'`
```
For Mainnet:
```
URL=`curl -L https://quicksync.io/axelar.json | jq -r '.[] |select(.file=="axelar-dojo-1-pruned")|.url'`
```
```
echo $URL
cd $HOME/.axelar/
wget -O - $URL | lz4 -d | tar -xvf -
```
### 7. Create services.
Use systemctl to set up services for axelard, tofnd, vald.
#### axelard
```
sudo tee <<EOF >/dev/null /etc/systemd/system/axelard.service
[Unit]
Description=Axelard Cosmos daemon
After=network-online.target
 
[Service]
User=$USER
ExecStart=/usr/bin/axelard start
Restart=always
RestartSec=3
LimitNOFILE=4096
 
[Install]
WantedBy=multi-user.target
EOF
 
cat /etc/systemd/system/axelard.service
sudo systemctl enable axelard
```
#### tofnd
```
sudo tee <<EOF >/dev/null /etc/systemd/system/tofnd.service
[Unit]
Description=Tofnd daemon
After=network-online.target
 
[Service]
User=$USER
ExecStart=/usr/bin/sh -c 'echo $KEYRING_PASSWORD | tofnd -m existing -d $HOME/.tofnd'
Restart=always
RestartSec=3
LimitNOFILE=4096
 
[Install]
WantedBy=multi-user.target
EOF
 
cat /etc/systemd/system/tofnd.service
sudo systemctl enable tofnd
```
#### vald
```
sudo tee <<EOF >/dev/null /etc/systemd/system/vald.service
[Unit]
Description=Vald daemon
After=network-online.target
[Service]
User=$USER
ExecStart=/usr/bin/sh -c 'echo $KEYRING_PASSWORD | /usr/bin/axelard vald-start --validator-addr $VALIDATOR_OPERATOR_ADDRESS --log_level debug --chain-id $CHAIN_ID --from broadcaster'
Restart=always
RestartSec=3
LimitNOFILE=4096
 
[Install]
WantedBy=multi-user.target
EOF
 
cat /etc/systemd/system/vald.service
sudo systemctl enable vald
```
### 8. Start all services.
Order of operations:
- axelard: ensure it's fully synced before proceeding
- tofnd: required for vald
- vald
```
sudo systemctl daemon-reload
sudo systemctl restart axelard
sudo systemctl restart tofnd
sudo systemctl restart vald
```
### 9. Check logs.
```
sed -i 's/#Storage=auto/Storage=persistent/g' /etc/systemd/journald.conf
sudo systemctl restart systemd-journald

sudo journalctl -u axelard.service -f -n 100
sudo journalctl -u tofnd.service -f -n 100
sudo journalctl -u vald.service -f -n 100
```
Check sync:
```
curl -s localhost:26657/status | jq .result | jq .sync_info
```
### 9. Register broadcaster proxy.
Note: Fund your validator and broadcaster accounts before proceeding.
```
axelard tx snapshot register-proxy $BROADCASTER_ADDRESS --from validator --chain-id $CHAIN_ID
```
### 9. Create validator.
```
IDENTITY="YOUR_KEYBASE_IDENTITY" # optional
AMOUNT=PUT_AMOUNT_OF_TOKEN_YOU_WANT_TO_DELEGATE
DENOM=uaxl
 
axelard tx staking create-validator --yes \
 --amount $AMOUNT$DENOM \
 --moniker $MONIKER \
 --commission-rate="0.10" \
 --commission-max-rate="0.20" \
 --commission-max-change-rate="0.01" \
 --min-self-delegation="1" \
 --pubkey="$(axelard tendermint show-validator)" \
 --from validator \
 -b block \
 --identity=$IDENTITY \
 --chain-id $CHAIN_ID
```
### 9. Register external chains
See [Support external chains](https://docs.axelar.dev/validator/external-chains)
```
axelard tx nexus register-chain-maintainer arbitrum optimism kava celo hero avalanche ethereum-2 fantom moonbeam polygon binance aurora  --from broadcaster --chain-id $CHAIN_ID --gas auto --gas-adjustment 1.4
```
### 9. Upgrade Process.
```
cd $HOME/binaries
```

```
AXELARD_RELEASE=<GIVE_VERSION>
TOFND_RELEASE=<GIVE_VERSION>
echo $AXELARD_RELEASE $TOFND_RELEASE
```
get axelard, tofnd binaries and rename
```
wget https://github.com/axelarnetwork/axelar-core/releases/download/$AXELARD_RELEASE/axelard-linux-amd64-$AXELARD_RELEASE
wget https://github.com/axelarnetwork/tofnd/releases/download/$TOFND_RELEASE/tofnd-linux-amd64-$TOFND_RELEASE
mv axelard-linux-amd64-$AXELARD_RELEASE axelard
mv tofnd-linux-amd64-$TOFND_RELEASE tofnd
```
make binaries executable and move
```
chmod +x *
sudo mv * /usr/bin/
```
check versions
```
axelard version
echo $AXELARD_RELEASE
tofnd --help
echo $TOFND_RELEASE
```
restart services
```
sudo systemctl restart axelard
sudo systemctl restart tofnd
sudo systemctl restart vald
```
check logs
```
sudo journalctl -u axelard.service -f -n 100
sudo journalctl -u tofnd.service -f -n 100
sudo journalctl -u vald.service -f -n 1000
```
