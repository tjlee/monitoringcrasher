__author__ = 'tjlee'

import argparse
import subprocess
import os
from time import sleep


def write_to_named_file(data_dir, file_name, data):
    tmp = os.path.join(data_dir, file_name)
    with open(tmp, 'w+') as f:
        f.write(data)
    return tmp


def execute_locally(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--loop", type=int, default=10, help="Command execution count (default: 10)")
    parser.add_argument("-o", "--output", default="../data/base/",
                        help="Output directory(have to be created) (default: ../data/base/)")
    parser.add_argument("-c", "--command", default="curl sas1-0064.search.yandex.net:11003/json/",
                        help="""Command to execute (default:curl sas1-0064.search.yandex.net:11003/json/)
                        base => curl sas1-0064.search.yandex.net:11003/json/
                        int => curl sas1-0856.search.yandex.net:11003/json/
                        meta => curl sas1-0294.search.yandex.net:11003/json/
                        upper => curl sas1-0053.search.yandex.net:11003/json/
                        balancer => curl balancer-ams00.yandex.ru:11003/json/""")

    args = parser.parse_args()

    i = 0
    while i < args.loop:
        i += 1
        data = execute_locally(args.command)
        file_name = write_to_named_file(args.output, "{0:05}".format(i), data)
        sleep(5) # to emulate golovan time-tick
        print(file_name)
