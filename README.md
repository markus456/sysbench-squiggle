# sysbench-squiggle

A simple [`sysbench`](https://github.com/akopytov/sysbench) visualizer that
displays the QPS as a graph and outputs max QPS at the end of the run.

## Usage

Pipe the output of sysbench to the script.

```
(cd /usr/share/sysbench && sysbench --mysql-host=127.0.0.1 --mysql-port=3000 \
    --mysql-user=maxuser --mysql-password=maxpwd --mysql-db=test \
    --threads=1 --time=60 --report-interval=1 --db-driver=mysql \
    /usr/share/sysbench/oltp_read_only.lua run) |./sysbench-squiggle.py
```
