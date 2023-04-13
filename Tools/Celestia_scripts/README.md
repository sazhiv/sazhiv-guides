# This script on PYTHON for Performance Analysis of Your Node

Script for analysis perfomance [analysis_perfomance.py](https://github.com/sazhiv/sazhiv-guides/blob/main/Tools/Celestia_scripts/analysis_perfomance.py)

In this way we see hardware performance of the machine your node is running on, bandwidth used, etc.

Example performance:

```CPU usage: 7.1%
Memory usage: 28.5%
Disk usage: 78.8%
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on enp8s0, link-type EN10MB (Ethernet), capture size 262144 bytes
10 packets captured
1923 packets received by filter
0 packets dropped by kernel
TCP packets: []
System log output: Apr 13 03:55:49 Ubuntu-2004-focal-64-minimal neard[412051]: 2023-04-13T01:55:49.346464Z  INFO stats: #033[1;33m#89454163 DgxBvkiG42dhmLnRTuDdVqmF5GDgjvkNxsHGXnXwtT8#033[0m#033[1;37m Validator | 100 validators#033[0m#033[1;36m 38 peers ⬇ 1.35 MB/s ⬆ 1.32 MB/s#033[0m#033[1;32m 0.90 bps 12.3 Tgas/s#033[0m#033[1;34m CPU: 43%, Mem: 9.71 GB#033[0m
Apr 13 03:55:51 Ubuntu-2004-focal-64-minimal celestia[1078746]: 2023-04-13T03:55:51.611+0200#011INFO#011header/store#011store/store.go:353#011new head#011{"height": 236049, "hash": "E42D93664BBC9B5FF666CD2574D5DC762613995E427D160A517D096AC177D870"}
Apr 13 03:55:51 Ubuntu-2004-focal-64-minimal celestia[1078746]: 2023-04-13T03:55:51.620+0200#011INFO#011das#011das/subscriber.go:35#011new header received via subscription#011{"height": 236049}
Apr 13 03:55:51 Ubuntu-2004-focal-64-minimal celestia[1078746]: 2023-04-13T03:55:51.724+0200#011INFO#011das#011das/worker.go:80#011finished sampling headers#011{"from": 236049, "to": 236049, "errors": 0, "finished (s)": 0.104014787}
Apr 13 03:55:59 Ubuntu-2004-focal-64-minimal neard[412051]: 2023-04-13T01:55:59.347665Z  INFO stats: #033[1;33m#89454172 7C2mJmbDoRaDNeKQ43s8MEjc4NhzJWenbBvw9LrDSgM1#033[0m#033[1;37m Validator | 100 validators#033[0m#033[1;36m 38 peers ⬇ 1.34 MB/s ⬆ 1.31 MB/s#033[0m#033[1;32m 0.90 bps 26.4 Tgas/s#033[0m#033[1;34m CPU: 44%, Mem: 9.73 GB#033[0m
Apr 13 03:56:02 Ubuntu-2004-focal-64-minimal celestia[1078746]: 2023-04-13T03:56:02.443+0200#011INFO#011header/store#011store/store.go:353#011new head#011{"height": 236050, "hash": "29E1210EF038EC19A39F6D9D1594969F79CC9EFF48D0905A4F870F71FADDF746"}
Apr 13 03:56:02 Ubuntu-2004-focal-64-minimal celestia[1078746]: 2023-04-13T03:56:02.459+0200#011INFO#011das#011das/subscriber.go:35#011new header received via subscription#011{"height": 236050}
Apr 13 03:56:02 Ubuntu-2004-focal-64-minimal celestia[1078746]: 2023-04-13T03:56:02.540+0200#011INFO#011das#011das/worker.go:80#011finished sampling headers#011{"from": 236050, "to": 236050, "errors": 0, "finished (s)": 0.080872913}
Apr 13 03:56:05 Ubuntu-2004-focal-64-minimal kernel: [29511142.010783] device enp8s0 entered promiscuous mode
Apr 13 03:56:05 Ubuntu-2004-focal-64-minimal kernel: [29511142.340918] device enp8s0 left promiscuous mode

Geekbench score: []
Peer connections: ['ESTABLISHED', 'ESTABLISHED', 'ESTABLISHED', 'ESTABLISHED', 'ESTABLISHED', 'ESTABLISHED', 'ESTABLISHED', 'ESTABLISHED', 'ESTABLISHED', 'ESTABLISHED', 'ESTABLISHED', 'ESTABLISHED', 'ESTABLISHED', 'ESTABLISHED', 'ESTABLISHED', 'ESTABLISHED', 'ESTABLISHED', 'ESTABLISHED', 'ESTABLISHED', 'ESTABLISHED', 'ESTABLISHED', 'ESTABLISHED', 'ESTABLISHED',]```



