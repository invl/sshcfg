import os
import urlparse

import argh
import paramiko


def get_sshconfig_path():
    return os.path.expanduser('~/.ssh/config')


def load_sshconfig():
    cfg = paramiko.SSHConfig()
    with open(get_sshconfig_path()) as f:
        cfg.parse(f)
    return [item for item in cfg._config if item['config']]


def write_sshconfig(lines):
    with open(get_sshconfig_path(), 'w') as f:
        for line in lines:
            f.write(line + '\n')


def dump_item(item):
    yield 'host {}'.format(item['host'][0])
    for k, v in item['config'].items():
        yield '    {} {}'.format(k, v)
    yield ''


def dump_sshconfig(cfg):
    for item in cfg:
        for line in dump_item(item):
            yield line


def to_uri(config):
    if 'user' in config:
        yield config['user']
        yield '@'
    yield config['hostname']
    if 'port' in config:
        yield ':'
        yield config['port']


def str_item(item):
    return '{}\t{}'.format(item['host'][0], ''.join(to_uri(item['config'])))


def parse_uri(uri):
    p = urlparse.urlsplit('ssh://' + uri)
    return {
        "hostname": p.hostname,
        "user": p.username,
        "port": p.port,
    }


def vacumm_dict(d):
    return dict((k, v) for k, v in d.items() if v)


def ls():
    for item in load_sshconfig():
        yield str_item(item)


def add(name, uri):
    cfg = load_sshconfig()
    cfg.append({"host": [name], "config": vacumm_dict(parse_uri(uri))})
    write_sshconfig(dump_sshconfig(cfg))


def rm(name):
    cfg = [item for item in load_sshconfig() if item['host'] != [name]]
    write_sshconfig(dump_sshconfig(cfg))


def main():
    argh.dispatch_commands([ls, add, rm])

if __name__ == '__main__':
    main()
