__author__ = 'tjlee'

import argparse


def generate_config(file_name, ip, start_port, number):
    with open(file_name, 'w+') as f:
        for item in range(start_port, start_port + number):
            to_write = "%s:%d\n" if item != int(start_port) + int(number) - 1 else "%s:%d"
            f.write(to_write % (ip, item))

    return file_name


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", default="../output/my_group.hosts.generated",
                        help="Generated configuration file name (default: ../output/my_group.hosts.generated)")
    parser.add_argument("-i", "--ip", default="178.154.159.91",
                        help="IP to generate config for. In format ip:port (default: 178.154.159.91)")
    parser.add_argument("-p", "--port", default=11004, type=int, help="Start port number (default: 11004)")
    parser.add_argument("-n", "--number", default=1, type=int, help="Number of port to generate config (default: 1)")

    args = parser.parse_args()

    generate_config(args.file, args.ip, args.port, args.number)
