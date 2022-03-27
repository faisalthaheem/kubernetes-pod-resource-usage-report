from kubernetes import client, config
import csv
import argparse

parser = argparse.ArgumentParser(description='Report pod resource usage.')
parser.add_argument('--context', help='The kubernetes context to query.')
parser.add_argument('--filename', help='The CSV report filename.', required=True)

args = parser.parse_args()

if args.context is not None:
    config.load_kube_config()
else:
    config.load_kube_config(context=args.context)
    
v1 = client.CoreV1Api()

columns = ['namespace','pod_name', 'container_name', 'request_cpu', 'request_mem', 'limit_cpu', 'limit_mem']
rows = []

ret = v1.list_pod_for_all_namespaces(watch=False)
for i in ret.items:
    
    for container in i.spec.containers:
        try:
            row = []
            row.extend(
                [
                    i.metadata.namespace,
                    i.metadata.name,
                    container.name
                ]
            )
            if container.resources.requests is not None:
 
                if 'cpu' in container.resources.requests:
                    row.append(container.resources.requests['cpu'])
                else:
                    row.append('?')
 
                if 'memory' in container.resources.requests:
                    row.append(container.resources.requests['memory'])
                else:
                    row.append('?')
            else:
                row.extend(['?','?'])

            if container.resources.limits is not None:
                    
                if 'cpu' in container.resources.limits:
                    row.append(container.resources.limits['cpu'])
                else:
                    row.append('?')
 
                if 'memory' in container.resources.limits:
                    row.append(container.resources.limits['memory'])
                else:
                    row.append('?')
            else:
                row.extend(['?','?'])
                
            rows.append(row) 

        except Exception as e:
            print("Error encountered while traversing.", e)
            print(container.resources)
            print("")
       
    
with open(args.filename,'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    
    csvwriter.writerow(columns)
    csvwriter.writerows(rows)
    
print("Done.")