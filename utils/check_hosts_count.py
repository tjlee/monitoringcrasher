__author__ = 'tjlee'

import argparse
import subprocess
import json
import math


def execute_locally(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    return output


def check_hosts_stats(host_count, percent):
    values = json.loads(execute_locally("""curl http://yasmstress-fol01:9003/stat/"""))

    aggr_3s = values['uptime_stat'].get('long_aggr_3s')
    aggr_4s = values['uptime_stat'].get('long_aggr_4s')
    aggr_5s = values['uptime_stat'].get('long_aggr_5s')

    errors = []

    if aggr_3s >= math.floor((host_count * percent) / 100):
        errors.append("Error. Deviation of aggr_3s=%s is more than %s %% from %s." % (aggr_3s, percent, host_count))
    if aggr_4s >= math.floor((host_count * percent) / 100):
        errors.append("Error. Deviation of aggr_4s=%s is more than %s %% from %s." % (aggr_4s, percent, host_count))
    if aggr_5s >= math.floor((host_count * percent) / 100):
        errors.append("Error. Deviation of aggr_5s=%s is more than %s %% from %s." % (aggr_5s, percent, host_count))

    if len(errors) > 0:
        exit(str(errors))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--deviation", type=int, default=1)
    parser.add_argument("-c", "--hosts", type=int, default=1)

    args = parser.parse_args()

    check_hosts_stats(args.hosts, args.deviation)



