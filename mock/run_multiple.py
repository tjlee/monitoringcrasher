__author__ = 'tjlee'

import sys
import subprocess
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", type=int, default=1,
                        help="Number of process to run simultaneously (default: 1)")
    parser.add_argument("-p", "--path", default="./mock/agent_mock_mc.py",
                        help="Path to process to run (default: ./agent_mock_mc.py)")
    parser.add_argument("-r", "--srange", type=int, default=11004,
                        help="Port number to start range from (default: 11004)")

    args = parser.parse_args()
    processes = []
    for port_number in range(args.srange, args.srange + args.number):
        process = subprocess.Popen([sys.executable, '%s' % args.path, '-p %d' % port_number])
        processes.append(process)

    for proc in processes:
        proc.wait()
