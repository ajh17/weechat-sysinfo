# weechat-sysinfo

A simple OS X system information script for weechat.

## Installation
    git clone https://github.com/ajh17/weechat-sysinfo.git
    cd weechat-sysinfo
    cp -R sysinfo.py data/ ~/.weechat/python/
    ln -s ~/.weechat/python/sysinfo.py ~/.weechat/python/autoload

## Dependencies
* WeeChat ≥ 0.4 (compiled with python support)
* psutil
    * Install with: `[sudo] pip install psutil`
