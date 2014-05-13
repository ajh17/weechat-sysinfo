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
SCRIPT_VERSION = '1.3'
SCRIPT_LICENSE = 'GPL3'
SCRIPT_DESC = 'Prints out system information out to the channel'
SCRIPT_COMMAND = "sysinfo"
BYTES = 1073741824

weechat.register(
    SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE,
    SCRIPT_DESC, SCRIPT_COMMAND, ''
)
hook = weechat.hook_command(
    "sysinfo", SCRIPT_DESC, "", "", "", "get_sysinfo", ""
)


def model_info():
    '''
    Get this Mac's model name
    '''
    model_command = (
        'defaults read ~/.weechat/python/sysinfo/data/MacintoshModels.plist |'
        'grep `sysctl -n hw.model` | awk -F\\\" {\'print $4\'}'
    )
    with os.popen(model_command) as mac_name:
        return "Model: {}".format(mac_name.readlines()[0].rstrip())


def cpu_info():
    '''
    Get the processor information, including the number of cores of this
    machine.
    '''
    cpu_command = (
        "sysctl machdep.cpu.brand_string |"
        "awk '{print $2,$3,$4,$5,$6,$7,$8,$9}'"
    )
    with os.popen(cpu_command) as cpu:
        with os.popen("sysctl -n machdep.cpu.core_count") as cores:
            cpu = re.sub("(\(R\)|\(TM\))", "", cpu.readlines()[0].rstrip())
            return "{} ({} cores)".format(cpu, cores.readlines()[0].rstrip())


def ram_info():
    '''
    Get the Memory size of this machine.
    '''
    with os.popen("sysctl -n hw.memsize") as mem:
        mem = int(mem.readlines()[0].rstrip()) / BYTES
        return "Memory: {:.2f} GB".format(mem)


def os_info():
    '''
    Get the OS information including the Build number.
    '''
    version_command = (
        "system_profiler SPSoftwareDataType | grep -Po '(?<=: )OS X.*'"
    )
    with os.popen(version_command) as version:
        return version.readlines()[0].rstrip()


def gpu_info():
    '''
    Get the GPU information of this machine.
    NOTE: Currently this only works with Macs with dual GPUs.
    '''
    gpu_command = (
        "system_profiler SPDisplaysDataType | egrep 'Ch|VR' | "
        "grep -Po '(?<=: ).*' | paste -s -d ' ' - |"
        "sed -E 's/([0-9]+ MB)/(\\1)/g' | sed 's/)/) +/'"
    )
    with os.popen(gpu_command) as gpu:
        return gpu.readlines()[0].rstrip()


def uptime_info():
    '''
    Get the amount of time that this machine has been on for, i.e. the uptime.
    '''
    with os.popen('uptime | grep -PZo "(?<=up )[^,]*"') as uptime:
        return "Uptime: {}".format(uptime.readlines()[0].rstrip())


def load_info():
    '''
    Get the current average CPU load of this machine.
    '''
    return "Average Load: {}%".format(psutil.cpu_percent())


def client_info():
    '''
    Get the IRC Client version information.
    '''
    return "Client: WeeChat {}".format(weechat.info_get("version", ""))


def get_sysinfo(data, buffer, args):
    '''
    Gets various system information related to this machine.
    '''
    item_list = [model_info, cpu_info, ram_info, gpu_info, uptime_info,
                 load_info, os_info, client_info]
    result = " ･ ".join([func() for func in item_list])
    weechat.command(buffer, result)

    return weechat.WEECHAT_RC_OK
