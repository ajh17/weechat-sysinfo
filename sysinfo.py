#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Author: Akshay Hegde <https://github.com/ajh17>
# NOTE: Only runs on OS X but you can fork this and modify it.
# NOTE2: The model information is currently partly hard coded.

try:
    import weechat
except ImportError as message:
    print "This script must be run under WeeChat."

import os
import re
import psutil

SCRIPT_NAME = 'sysinfo'
SCRIPT_AUTHOR = 'Akshay Hegde'
SCRIPT_VERSION = '1.0'
SCRIPT_LICENSE = 'GPL3'
SCRIPT_DESC = 'Prints out system information out to the channel'
SCRIPT_COMMAND = "sysinfo"

weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE,
                 SCRIPT_DESC, SCRIPT_COMMAND, '')
hook = weechat.hook_command("sysinfo", SCRIPT_DESC, "", "", "",
                            "get_sysinfo", "")


def model_info():
    model_command = "system_profiler SPHardwareDataType |"
    model_command += "egrep 'Model Name' | cut -d':' -f2 | sed 's/ //'"
    model = os.popen(model_command).readlines()[0].rstrip()
    return model + " (15-inch Retina, Late 2013)"


def cpu_info():
    command = "sysctl machdep.cpu.brand_string | awk\
        '{print $2,$3,$4,$5,$6,$7,$8,$9}'"
    cpu = os.popen(command).readlines()[0].rstrip()
    cores = os.popen("sysctl -n machdep.cpu.core_count").readlines()[0]
    cpu = re.sub("(\(R\)|\(TM\))", "", cpu)
    return cpu + " (" + cores.rstrip() + " cores)"


def ram_info():
    command = "sysctl -n hw.memsize"
    mem = os.popen(command).readlines()[0].rstrip()
    mem = int(mem) / 1048576 / 1024
    return "Memory: " + str(float(mem)) + " GB"


def os_info():
    version_command = "system_profiler SPSoftwareDataType"
    version_command += "| grep System\ Version | cut -d \":\" -f 2 |"
    version_command += "sed 's/(/(Build /' | sed 's/ //'"
    version = os.popen(version_command).readlines()[0].rstrip()
    return version


def gpu_info():
    gpu_command = "system_profiler SPDisplaysDataType | egrep 'Chip|VR' | "
    gpu_command += "cut -d ':' -f 2 | sed 's/ //' | paste -s -d ',' - | "
    gpu_command += "sed 's/,/ \(/' | sed 's/,/\) + /' |"
    gpu_command += "sed 's/,/ \(/' | sed 's/$/\)/'"
    gpu = os.popen(gpu_command).readlines()[0].rstrip()
    return gpu


def uptime_info():
    uptime = os.popen('~/.bin/uptime.zsh').readlines()
    uptime = uptime[0]
    return "Uptime: " + uptime.rstrip()


def load_info():
    load = psutil.cpu_percent()
    result = str(load) + "%"
    return "Avg. Load: " + result


def client_info():
    return "WeeChat " + weechat.info_get("version", "")


def get_sysinfo(data, buffer, args):
    separator = " ･ "
    computer_model, cpu_model, memory = model_info(), cpu_info(), ram_info()
    gpu, system_info, load = gpu_info(), os_info(), load_info()
    uptime, client = uptime_info(), client_info()

    result_string = "Model: " + computer_model + separator
    result_string += cpu_model + separator + memory + separator
    result_string += gpu + separator + uptime + separator
    result_string += load + separator + system_info + separator
    result_string += "IRC Client: " + client

    weechat.command(buffer, result_string)
    return weechat.WEECHAT_RC_OK
