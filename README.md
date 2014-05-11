# weechat sysinfo

A simple system information script for weechat.

## Installation
    git clone https://github.com/ajh17/weechat-sysinfo.git
    cd weechat-sysinfo && cp sysinfo.py ~/.weechat/python/
    cd !$ && ln -s sysinfo.py autoload

## Dependencies
* psutil
    * Install with: `[sudo] pip install psutil`

## Caveats
* Only works with OS X
* Some of it is hard-coded. Fork and modify the script if you wish.
