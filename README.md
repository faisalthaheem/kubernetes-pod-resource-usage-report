# Kubernetes Pod Resource Usage Report

A handy python script to list resource (limits/requests) usage by pods. A report containing namespace, pod name and resource usage is written to a csv file.

# To use

Install dependencies
```bash
pip3 install -r requirements.txt
```

Then, use as below to get data from current context
```bash
python3 report.py --filename my_cluster_report.csv
```

In case you hae multiple clusters, you can specify the context as follows
```bash
python3 report.py --filename my_other_cluster_report.csv --context my_other_cluster
```