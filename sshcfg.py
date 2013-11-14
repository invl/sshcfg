import os
import urlparse

import argh
import paramiko


def to_uri(config):
    if 'user' in config:
        yield config['user']
        yield '@'
    yield config['hostname']
    if 'port' in config:
        yield ':'
        yield config['port']


def ls():
    for item in load_sshconfig():
        if item['config']:
            print str_item(item)


def str_item(item):
    return '{}\t{}'.format(item['host'][0], ''.join(to_uri(item['config'])))


def load_sshconfig():
    cfg = paramiko.SSHConfig()
    with open(os.path.expanduser('~/.ssh/config')) as f:
        cfg.parse(f)
    return cfg._config


def parse_uri(uri):
    p = urlparse.urlsplit('ssh://' + uri)
    return {
        "hostname": p.hostname,
        "user": p.username,
        "port": str(p.port),
    }


def vacumm_dict(d):
    return dict((k, v) for k, v in d.items() if v)


def dump_item(item):
    print 'host', item['host'][0]
    for k, v in item['config'].items():
        print '    ' + k, v
    print


def add(name, uri):
    cfg = load_sshconfig()
    newitem = {"host": [name], "config": vacumm_dict(parse_uri(uri))}
    cfg.append(newitem)
    for item in cfg:
        if item['config']:
            dump_item(item)


def rm(name):
    cfg = load_sshconfig()
    for item in cfg:
        if item['config'] and item['host'] != [name]:
            dump_item(item)


def main():
    argh.dispatch_commands([ls, add, rm])

if __name__ == '__main__':
    main()
