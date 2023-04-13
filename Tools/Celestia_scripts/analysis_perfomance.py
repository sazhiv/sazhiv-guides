# This script on PYTHON for Performance Analysis of Your Node
                                                                                     
import psutil
import subprocess
import re

# Monitor resource utilization
cpu_usage = psutil.cpu_percent(interval=1)
mem_usage = psutil.virtual_memory().percent
disk_usage = psutil.disk_usage('/').percent

print(f'CPU usage: {cpu_usage}%')
print(f'Memory usage: {mem_usage}%')
print(f'Disk usage: {disk_usage}%')

# Analyze network traffic
tcpdump_proc = subprocess.Popen(['tcpdump', '-i', 'enp8s0', '-c', '10'], stdout=subprocess.PIPE)
tcpdump_output = tcpdump_proc.stdout.read().decode()
tcpdump_packets = re.findall(r'\d+ packets', tcpdump_output)
print(f'TCP packets: {tcpdump_packets}')

# Check system logs
tail_proc = subprocess.Popen(['tail', '-n', '10', '/var/log/syslog'], stdout=subprocess.PIPE)
tail_output = tail_proc.stdout.read().decode()
print(f'System log output: {tail_output}')

# Benchmark node performance
geekbench_proc = subprocess.Popen(['/usr/local/bin/geekbench6', '--cpu', '--compute'], stdout=subprocess.PIPE)
geekbench_output = geekbench_proc.stdout.read().decode()
geekbench_score = re.findall(r'Single-Core Score:\s+(\d+)\nMulti-Core Score:\s+(\d+)', geekbench_output)
print(f'Geekbench score: {geekbench_score}')

# Monitor blockchain-specific metrics
# TODO: Add code to monitor blockchain-specific metrics

# Analyze peer connections
netstat_proc = subprocess.Popen(['netstat', '-an'], stdout=subprocess.PIPE)
netstat_output = netstat_proc.stdout.read().decode()
peer_connections = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+\s+\d+\.\d+\.\d+\.\d+:\d+\s+(ESTABLISHED|TIME_WAIT)', netstat_output)
print(f'Peer connections: {peer_connections}')


