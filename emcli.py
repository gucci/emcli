#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = "Gucci-Office"

import os
import sys
import configparser
import argparse
import yagmail
import select

from storage import Storage
from logger import get_logger

logger = get_logger()

def get_argparse():
    parser = argparse.ArgumentParser(description='A email client in terminal')
    parser.add_argument('-s',action='store',dest='subject',required=True,help='specify a subject (must be in quotes if it has spaces')
    parser.add_argument('-b',action='store',dest='body',required=False,help='body content in the message')
    parser.add_argument('-a',action='store',nargs='*',dest='attaches',required=False,help='attach file(s) to the message')
    parser.add_argument('-f',action='store',dest='conf',required=False,help='specify an alternate .emcli.cnf file')
    parser.add_argument('-r',action='store',nargs='*',dest='recipients',required=True,help='recipient who you are sending the email to')
    parser.add_argument('-v',action='version',version='%(prog)s 0.1')
    return parser.parse_args()


def get_config_file(config_file):
    if config_file is None:
        config_path = os.path.expanduser('~')
        config_file = os.path.join(config_path,'.emcli.cnf')
    return config_file

def get_meta_from_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    meta = Storage()
    for key in ['smtp_server','smtp_port','username','password']:
        try:
            val = config.get('DEFAULT',key)
        except (configparser.NoSectionError,configparser.NoOptionError) as err:
            logger.error(err)
            raise SystemExit(err)
        else:
            meta[key] = val
    return meta

def get_email_content():
    if not sys.stdin.isatty():
        return [sys.stdin.read()]
    else:
        return list()

def send_email(meta):
    content = get_email_content()
    with yagmail.SMTP(user=meta.username, password=meta.password,
                      host=meta.smtp_server, port=int(meta.smtp_port)) as yag:
        logger.info('ready to send email "{0}" to {1}'.format(meta.subject, meta.recipients))
        if meta.attaches is None:
            content = [meta.body] + content
        else:
            content = [meta.body] + content
            content = content + meta.attaches
        meta.recipients = meta.recipients[0].split(',')
        for recipient in meta.recipients:
            yag.send(recipient, meta.subject, content)

def main():
    parser = get_argparse()
    config_file = get_config_file(parser.conf)

    if not os.path.exists(config_file):
        logger.error('{0} is not exists'.format(config_file))
        raise SystemExit()
    else:
        meta = get_meta_from_config(config_file)

    meta.subject = parser.subject
    meta.recipients = parser.recipients
    meta.body = parser.body
    meta.attaches = parser.attaches[0]
    meta.attaches = meta.attaches.split(',')

    if meta.attaches is not None:
        for attach in meta.attaches:
            if not os.path.exists(attach):
                logger.error('{0} is not exists'.format(attach))
                raise SystemExit()
    send_email(meta)

if __name__ == '__main__':
    main()
