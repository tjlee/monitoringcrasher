__author__ = 'tjlee'

from os import path, listdir
from random import shuffle

import argparse
import memcache

from memcache_data_loader import get_file_contents


def read_mixed_files_to_array(paths_to_data_and_amount):
    """
    [path_to_data1, path_to_data2,..., path_to_dataN]
    """
    file_contents = []
    iterator = 1

    for data_item in paths_to_data_and_amount:
        file_names = map(lambda x: path.join(data_item, x), listdir(data_item))

        for file_name in file_names:
            file_contents.append((path.basename("{0:05}".format(iterator)), get_file_contents(file_name)))
            iterator += 1

    shuffle(file_contents) # mixing data

    return file_contents


def parse_input_data_to_path_array(data):
    """
    chunk1;chunk2;chunk3
    or
    chunk1
    or
    chunk1;chunk2;chunk (that's why filter)
    => ['../data/chunk1', '../data/chunk2', '../data/chunk3']
    """
    return map(lambda x: path.join("../data", x),
               filter(lambda x: x != '', data.split(';')))


def load_mix_data_to_memcache(host, port, path_to_data):
    mc = memcache.Client(['%s:%d' % (host, port)], debug=0)

    for file_data in read_mixed_files_to_array(path_to_data):
        mc.set(file_data[0], file_data[1])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-dr", "--datarange", default="base;int;", help="Itypes to upload separated by ';' (default: 'base;int;'")
    parser.add_argument("-mh", "--memhost", default="127.0.0.1", help="Memcache server host (default: 127.0.0.1)")
    parser.add_argument("-mp", "--memport", type=int, default=11000, help="Memcache server port (default: 11000)")
    args = parser.parse_args()

    load_mix_data_to_memcache(args.memhost, args.memport, parse_input_data_to_path_array(args.datarange))
