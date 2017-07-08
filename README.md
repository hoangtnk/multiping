# Description
Ping multiple destinations and print out the statistics including packets sent, packets lost... and the associated date time when those packets were lost.

# Installation
Install the colorama module:
```
pip install colorama
```

# Usage
Assign execute permission to the script:
```
$ chmod a+x multiping.py
```

Show the available options:
```
$ ./multiping.py --help
usage: multiping.py [-h] [--version] host [host ...]

HoangTNK's multiping v1.0

positional arguments:
  host        IP/hostname of destination

optional arguments:
  -h, --help  show this help message and exit
  --version   show program's version number and exit
```

Sample output:
```
$ ./multiping.py cisco.com google.com zing.vn

Ping logs will be recorded to '/home/hoangtnk/Logs' directory.

Sending pings to the listed destinations...

Press 'Ctrl-C' to stop the ping and view statistics.

^C

Analyzing ping results. Please wait...

========================== BEGIN OF STATISTICS ==========================

+ CISCO.COM:
Total packets sent: 17
Total packets received: 17
Total packets lost: 0 (0%)
Minimum latency: 245.071 ms
Maximum latency: 905.690 ms
Average latency: 377.002 ms

+ GOOGLE.COM:
Total packets sent: 17
Total packets received: 17
Total packets lost: 0 (0%)
Minimum latency: 57.807 ms
Maximum latency: 1063.761 ms
Average latency: 189.010 ms

+ ZING.VN:
Total packets sent: 17
Total packets received: 17
Total packets lost: 0 (0%)
Minimum latency: 5.226 ms
Maximum latency: 2285.608 ms
Average latency: 388.035 ms

=========================== END OF STATISTICS ===========================
```
