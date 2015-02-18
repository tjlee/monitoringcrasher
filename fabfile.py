__author__ = 'tjlee'

import os

from fabric.api import *

from utils.hosts_config_generator import generate_config


# 178.154.159.91 - yasmstress-fol02 (agents)
# 178.154.159.68 - yasmstress-fol01  (server)
env.roledefs = {'agent': ['178.154.159.91'], 'server': ['178.154.159.68']}

env.user = 'teamcity'
env.password = 'Cleph8OvOwd'

server_launch_dir = "/etc/init.d/"
server_config_dir = "/place/yasm/apps/conf/"
agent_mock_launch_dir = "/home/teamcity/agent_mock"
agent_mock_memcached_dir = "/home/teamcity/agent_mock/memcacheloader"
server_yasmserver5_dir = "/place/yasm/apps/git/yasmserver5"
server_yasmutil_dir = "/place/yasm/apps/lib/yasmutil"
server_yasmconf_dir = "/place/yasm/apps/conf/"
server_yasmconf_conf_dir = "/place/yasm/apps/conf/yasmconf/"
server_yasmscripts_dir = "/place/yasm/apps/git/scripts/" #need to copy to git/scripts


@task
@roles('agent')
def run_agent_mock(start_port=11004, port_count=1):
    with cd(agent_mock_launch_dir):
        run("python ./mock/run_multiple.py -n=%d -r=%d" % (int(port_count), int(start_port)))


@task
@roles('agent')
def stop_agent_mock():
    run("sudo kill $(pgrep -f run_multiple.py | grep -v ^$$\$)", warn_only=True)


@task
@roles('agent')
def launch_memcached_server(memcached_port=11000, count=4096, data_dir="../data/base/"):
    with cd(agent_mock_memcached_dir):
        size_mb = int(run("du -sm %s" % data_dir).split()[0])
        run("sudo memcached -u teamcity -d -m %d -p %d -c %d" % (size_mb * 2, int(memcached_port), int(count) + 100))
        run("python memcache_data_loader.py -mp=%d -d=%s" % (int(memcached_port), data_dir))


@task
@roles('agent')
def stop_specified_agent_mock(start_port, port_count):
    run("ps -ef | awk '/run_multiple.py -n=%d -r=%d/{print $2}' | xargs sudo kill" % (int(port_count), int(start_port)))


@task
@roles('agent')
def load_mix_data_to_memcached(memcached_port=11000, itypes="base;int"):
    with cd(agent_mock_memcached_dir):
        run("python memcache_mix_data_loader.py -mp=%s -dr=\"%s\"" % (
            memcached_port, itypes))


@task
@roles('agent')
def stop_memcached_server():
    run("sudo kill $(pgrep -f memcached | grep -v ^$$\$)", warn_only=True)


@task
@roles('agent')
def copy_crawled_data_to_agent(data_dir="../data/base/", target_dir="/home/teamcity/data_test/"):
    put(data_dir, target_dir, use_sudo=True, mirror_local_mode=True)


@task
@roles('server')
def stop_golovan_server():
    with cd(server_launch_dir):
        run("sudo ./yasmserver stop")


@task
@roles('server')
def start_golovan_server():
    with cd(server_launch_dir):
        run("sudo ./yasmserver start")


@task
@roles('server')
def restart_golovan_server():
    with cd(server_launch_dir):
        run("sudo ./yasmserver restart")


@task
@roles('server')
def change_my_group_conf(start_port=11004, port_count=1):
    generate_config("./output/my_group.hosts.generated", env.roledefs['agent'][0], int(start_port), int(port_count))
    with cd(server_config_dir):
        run("sudo rm my_group.hosts")
    put("./output/my_group.hosts.generated", "/place/yasm/apps/conf/my_group.hosts", use_sudo=True,
        mirror_local_mode=True)


@task
@roles('server')
def change_workers_count_in_instances_conf(workers=28):
    """
    Changes MY_GROUP||/place/yasm/apps/run/my_group.pid||9003||True||cat /place/yasm/apps/conf/my_group.hosts||/5/0||%workes
    """
    instances_string = "sudo echo 'MY_GROUP||/place/yasm/apps/run/my_group.pid||9003||True||cat /place/yasm/apps/conf/my_group.hosts||/5/0||%d' > instances.conf"

    with cd(server_config_dir):
        run("sudo rm instances.conf")
        run(instances_string % int(workers))


@task
@roles('server')
def cp_yasmscripts_to_server():
    run("sudo rm -rf %s" % server_yasmscripts_dir)
    run("sudo mkdir -p %s" % server_yasmscripts_dir)
    put("./scripts", "/place/yasm/apps/git/", use_sudo=True, mirror_local_mode=True)


@task
@roles('server')
def cp_yasmutils_to_server():
    run("sudo rm -rf %s" % server_yasmutil_dir)
    run("sudo mkdir -p %s" % server_yasmutil_dir)
    put("./yasmutil", "/place/yasm/apps/lib/", use_sudo=True, mirror_local_mode=True)


@task
@roles('server')
def cp_yasmserver_to_server():
    run("sudo rm -rf %s" % server_yasmserver5_dir)
    run("sudo mkdir -p %s" % server_yasmserver5_dir)
    put("./yasmserver5", "/place/yasm/apps/git/", use_sudo=True, mirror_local_mode=True)
    

@task
@roles('server')
def copy_yasmconf_to_server(path_to_yasmconf="yasm.conf", revision="HEAD"):
    put(path_to_yasmconf, "/place/yasm/apps/conf/yasmconf/yasmconf-%s" % revision, use_sudo=True,
        mirror_local_mode=True)


@task
@roles('server')
def change_yasmconf_symlink(filename):
    with cd(server_yasmconf_dir):
        run("sudo rm yasm.conf")
        run("sudo ln -s %s yasm.conf" % os.path.join(server_yasmconf_conf_dir, filename))


@task
@roles("server")
def update_server_data_protocol(protocol):
    with cd(server_yasmconf_dir):
        run("sudo sed -i -r s/'yasmagent_data_protocol = .+'/'yasmagent_data_protocol = {0}'/ worker_aggr.conf".format(
            protocol))
