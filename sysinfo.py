#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Akshay Hegde <https://github.com/ajh17>

try:
    import weechat
except ImportError:
    print "This script must be run under WeeChat."

import os
import re
import psutil

SCRIPT_NAME = 'sysinfo'
SCRIPT_AUTHOR = 'Akshay Hegde'
SCRIPT_VERSION = '1.2'
SCRIPT_LICENSE = 'GPL3'
SCRIPT_DESC = 'Prints out system information out to the channel'
SCRIPT_COMMAND = "sysinfo"

weechat.register(
    SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE,
    SCRIPT_DESC, SCRIPT_COMMAND, ''
)
hook = weechat.hook_command(
    "sysinfo", SCRIPT_DESC, "", "", "", "get_sysinfo", ""
)


def model_info():
    plist_path = '~/.weechat/python/sysinfo/data/MacintoshModels.plist'
    mac_name = os.popen(
        'defaults read ' + plist_path + ' | '
        'grep `sysctl -n hw.model` | awk -F\\\" {\'print $4\'}'
    ).readlines()[0].rstrip()
    return "Model: {}".format(mac_name)


def cpu_info():
    cpu_command = (
        "sysctl machdep.cpu.brand_string |"
        "awk '{print $2,$3,$4,$5,$6,$7,$8,$9}'"
    )
    cpu = os.popen(cpu_command).readlines()[0].rstrip()
    cores = os.popen("sysctl -n machdep.cpu.core_count").readlines()[0]
    cpu = re.sub("(\(R\)|\(TM\))", "", cpu)
    return cpu + " (" + cores.rstrip() + " cores)"


def ram_info():
    memory_command = "sysctl -n hw.memsize"
    mem = os.popen(memory_command).readlines()[0].rstrip()
    mem = int(mem) / 1048576 / 1024
    return "Memory: " + str(float(mem)) + " GB"


def os_info():
    version_command = (
        "system_profiler SPSoftwareDataType | grep -Po '(?<=: )OS X.*'"
    )
    version = os.popen(version_command).readlines()[0].rstrip()
    return version


def gpu_info():
    gpu_command = (
        "system_profiler SPDisplaysDataType | egrep 'Chip|VR' | "
        "cut -d ':' -f 2 | sed 's/ //' | paste -s -d ',' - | "
        "sed 's/,/ \(/' | sed 's/,/\) + /' |"
        "sed 's/,/ \(/' | sed 's/$/\)/'"
    )
    gpu = os.popen(gpu_command).readlines()[0].rstrip()
    return gpu


def uptime_info():
    uptime = os.popen('uptime | grep -PZo "(?<=up )[^,]*"').readlines()[0]
    return "Uptime: " + uptime.rstrip()


def load_info():
    return "Average Load: " + str(psutil.cpu_percent()) + "%"


def client_info():
    return "Client: WeeChat {}".format(weechat.info_get("version", ""))


def get_sysinfo(data, buffer, args):
    item_list = [model_info, cpu_info, ram_info, gpu_info, uptime_info,
                 load_info, os_info, client_info]

    result = " ･ ".join([func() for func in item_list])
    weechat.command(buffer, result)

    return weechat.WEECHAT_RC_OK
