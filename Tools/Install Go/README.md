### 1. Update your server.
```
sudo apt update && sudo apt upgrade -y
```
```
sudo apt install make clang pkg-config libssl-dev libclang-dev build-essential git curl ntp jq llvm tmux unzip cmake -y
```
### 2. If you installing Go on clear server you need input following commands.
```
cd /usr/src
sudo rm -Rf go*
sudo wget https://go.dev/dl/`curl -s https://go.dev/dl/?mode=json | jq -r '.[0].version'`.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go*.linux-amd64.tar.gz
cat <<EOF >> ~/.profile
export GOROOT=/usr/local/go
export GOPATH=$HOME/go
export GO111MODULE=on
export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin
EOF
source ~/.profile
go version
sudo rm -rf /usr/src/go*.linux-amd64.tar.gz
cd ~
```

### 3. If you would like update your Go you need input following commands.
```
sudo rm -rvf /usr/local/go/
```
```
sudo rm -rvf go
```
Than proceed to the step 2.
### 4. If you would like delete your Go from your server you need input following commands.
```
sudo rm -rvf /usr/local/go/
```
```
sudo rm -rvf go
```
