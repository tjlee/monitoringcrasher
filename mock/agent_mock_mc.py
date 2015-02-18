__author__ = 'tjlee'

import argparse
import cPickle
import json
import memcache

from flask import Flask, Response

app = Flask(__name__)
# there is no method to get all memcacheloader keys collection
# used to return data in the same order as it was recorded
# if there is no data for key requested None is returned
key_iterator = 0


def get_value_from_cache():
    global key_iterator
    key_iterator += 1
    return mc.get("{0:05}".format(key_iterator)) or "{}"


@app.route("/json/")
def json_handler():
    return Response(response=get_value_from_cache())

@app.route("/pickle/")
def pickle_handler():
    return Response(response=cPickle.dumps(json.loads(get_value_from_cache())))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=11004, help="Agent mock port (default: 11004)")
    parser.add_argument("-mh", "--memhost", default="127.0.0.1", help="Memcache server host (default: 127.0.0.1)")
    parser.add_argument("-mp", "--memport", type=int, default=11000, help="Memcache server port (default: 11000)")
    args = parser.parse_args()

    mc = memcache.Client(['%s:%d' % (args.memhost, args.memport)], debug=0)
    app.run(host="0.0.0.0", port=args.port)
