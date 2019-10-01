#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import ConfigParser
import argparse
import os
import subprocess

import boto3

home = os.path.expanduser("~")
key_root_path = home

parser = argparse.ArgumentParser()
parser.add_argument('-r', help='assign a region', dest='region')
parser.add_argument('-c', help='copy deploy key?(y or n)', dest='flag_cpkey')
parser.add_argument('-l', help='list all instances', dest='listins')

args = parser.parse_args()

config = ConfigParser.ConfigParser()
config.read('%s/.aws/config' % home)
region_name = config.get('default', 'region')
flag_cpkey = True
flag_listins = True
if not args.region is None:
    region_name = args.region
if args.flag_cpkey is None:
    flag_cpkey = False
if args.listins is None:
    flag_listins = False

# region_name = 'us-east-1'
print('\033[1;31;406m Region\033[0m: %s' % region_name)
client = boto3.client('emr', region_name=region_name)


def add_cluster_tags():
    res = client.list_clusters()
    cluster_list = res['Clusters']
    ready_count = 0

    for i in range(len(cluster_list)):
        if 'TERMINATED' not in cluster_list[i]['Status']['State']:
            cmd = 'aws emr add-tags --resource-id %s --tags auto-stop="no" auto-delete="no"' % (cluster_list[i]['Id'])
            print("cmd: %s" % (cmd))
            retcode = subprocess.call(cmd, shell=True)

if __name__ == '__main__':
    add_cluster_tags()
