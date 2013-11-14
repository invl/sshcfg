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
            yield str_item(item)


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
        "port": p.port,
    }


def vacumm_dict(d):
    return dict((k, v) for k, v in d.items() if v)


def dump_item(item):
    yield 'host {}'.format(item['host'][0])
    for k, v in item['config'].items():
        yield '    {} {}'.format(k, v)
    yield ''


def add(name, uri):
    cfg = load_sshconfig()
    cfg.append({"host": [name], "config": vacumm_dict(parse_uri(uri))})
    return dump_sshconfig(cfg)


def dump_sshconfig(cfg):
    for item in cfg:
        if item['config']:
            for line in dump_item(item):
                yield line


def rm(name):
    cfg = [item for item in load_sshconfig() if item['host'] != [name]]
    return dump_sshconfig(cfg)


def main():
    argh.dispatch_commands([ls, add, rm])

if __name__ == '__main__':
    main()
