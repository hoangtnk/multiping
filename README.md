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
(4 packets lost) at 22:17:47 08/07/2017
Total packets sent: 17
Total packets received: 13
Total packets lost: 4 (23%)
Minimum latency: 243.023 ms
Maximum latency: 378.873 ms
Average latency: 293.359 ms

+ GOOGLE.COM:
(4 packets lost) at 22:17:47 08/07/2017
Total packets sent: 17
Total packets received: 13
Total packets lost: 4 (23%)
Minimum latency: 56.288 ms
Maximum latency: 65.612 ms
Average latency: 58.119 ms

+ ZING.VN:
(4 packets lost) at 22:17:46 08/07/2017
Total packets sent: 17
Total packets received: 13
Total packets lost: 4 (23%)
Minimum latency: 3.538 ms
Maximum latency: 15.257 ms
Average latency: 6.614 ms

=========================== END OF STATISTICS ===========================
```
_**Note:** Modify the log directory in the script to suit your system_
