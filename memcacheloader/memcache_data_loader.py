__author__ = 'tjlee'

from os import path, listdir

import argparse
import memcache


def get_file_contents(file_name):
    with open(file_name, "r") as tmp_file:
        data = tmp_file.read().replace('\n', '')
    return data


def read_files_to_array(path_to_data):
    file_names = map(lambda x: path.join(path_to_data, x), listdir(path_to_data))

    file_contents = []
    for file_name in file_names:
        file_contents.append((path.basename(file_name), get_file_contents(file_name)))

    return file_contents


def load_data_to_memcache(host, port, path_to_data):
    mc = memcache.Client(['%s:%d' % (host, port)], debug=0)

    for file_data in read_files_to_array(path_to_data):
        mc.set(file_data[0], file_data[1])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", default="../data/base/", help="Data files dir (default: ../data/base/)")
    parser.add_argument("-mh", "--memhost", default="127.0.0.1", help="Memcache server host (default: 127.0.0.1)")
    parser.add_argument("-mp", "--memport", type=int, default=11000, help="Memcache server port (default: 11000)")
    args = parser.parse_args()

    load_data_to_memcache(args.memhost, args.memport, args.data)
