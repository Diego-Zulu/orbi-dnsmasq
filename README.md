# orbi-dnsmasq

[![PyPI version](https://badge.fury.io/py/orbi-dnsmasq.svg)](https://badge.fury.io/py/orbi-dnsmasq)

Python command to update dnsmasq configuration file and / or set hosted hosts file on your Netgear Orbi router.

## Description

### Inspiration

If you own a [Netgear Orbi](https://www.netgear.com/orbi/), you should know that its OS is based on [OpenWrt](https://openwrt.org/).
This means that we could use telnet to tap into some of the features that haven't been made available through the web GUI.
I was really interested in the [`dnsmasq`](https://en.wikipedia.org/wiki/Dnsmasq) capabilities to set up "Router based 
ad-blocking" to reduce ads on my whole network, so I decided to try and config that into my router after reading about it on 
[hackingthenetgearorbi](https://hackingthenetgearorbi.wordpress.com/).

There was just one problem: **Configs done to the orbi will be erased when it turns off**.

Because of this, I wanted to create a "fire and forget" command that I could run comfortably whenever I was feeling like it.
I also thought it would be neat if people without technical knowledge would be able to run it too.

And that's the reason I created `orbi-dnsmasq`, and why you are reading this now!

### Steps this command takes

- Asks for router password (note: the password is not stored in any way, you'll need to re-enter it every time).
- Turns on telnet on the debug Orbi GUI if `-t` flag was supplied.
- Telnet into Orbi.
- Replace `/etc/dnsmasq.conf` with a custom configuration file specified by `-c <path>`
- Downloads hosts file if `-d` was supplied (you can specify a custom url with the `-u <url>` flag, or check the default one I'm using 
on [someonewhocares.org](https://someonewhocares.org/hosts/)).
- Deletes the `no-hosts` line to active dnsmasq.
- Reboots Orbi's dns.
- Turns off telnet  on the debug Orbi GUI if `-t` flag was supplied.

## Getting Started

### Running in Docker

This is the easiest way to run, all you need is Docker installed an run:
```
docker build -t orbi-dnsmasq . && \
docker run -it --rm orbi-dnsmasq <parameters>
```
You only need the first line on the first run or if you change any Python files.

If you want to upload a custom configuration file, you'll have to expose it as Docker volume, ie:
```
docker run -it --rm -v <full path to dnsmasq.conf>:/tmp/dnsmasq.conf orbi-dnsmasq -p $orbipw -a 192.168.21.1 -t -c /tmp/dnsmasq.conf
```


### Prerequisites (without Docker)

First, make sure python is already installed on your system by opening the interactive environment by running on your terminal:
 
```
python
```

I've tested both Python 2.7 and 3.7, so I believe any version from 2.7 onwards should work.
If you don't have Python installed, please [download it from the official website](https://www.python.org/downloads/). 

After that, any terminal or equivalent with telnet and vim should be enough to run this correctly, but do let me know 
if you find any problems!

### Installing

Simply run:

```
pip install orbi-dnsmasq
```

And then if your Orbi has [telnet already on](https://oldwiki.archive.openwrt.org/toh/netgear/telnet.console), just run it with:
```
orbi-dnsmasq
```

After this, just enter a site which would usually end up filled with ads and see if the config worked. I usually test 
this step out with [Speedtest by Ookla](https://www.speedtest.net/), but you can use whichever one you want. _Note: 
Not every ad will be blocked, youtube ads still seem to be showing up for example. Nevertheless, a lot of dangerous sites and ads won't
 be shown._

Also, **don't worry if you end up running this command twice**. I made sure it does not fail if the config was already in place.

#### Auto turn on telnet before command, and turn it off after

If you don't like leaving telnet port open when not using it, you can use the `-t` parameter to automatically toggle Telnet on and off after work is done.

After that, run:

```
orbi-dnsmasq -t
```

## Known issues
Sometimes authentication will fail and you'll see a `ts not found, retry in a minute or two` error. Normally retrying works.

## Possible things to add:

- ~~Read password from ENV var, don't ask it if already found.~~ You can provide the `admin` password with `-p <password>` parameter.
- Flag option to set username to connect with, use admin as default (is this even necessary?).
- Create Telnet object with telnet_write methods, cleaning up the code.
- Understand why authentication fails every now and then and fix it.
- Improve `README.md`
- Unit testing? (does it even makes sense? All telnet communications would need to be mocked)

## Acknowledgments

- This project wouldn't have been possible without [hackingthenetgearorbi](https://hackingthenetgearorbi.wordpress.com/), 
so please show them some love!
- Also check out [hackingthenetgearorbi creator's github](https://github.com/tumescentrubor/Orbi-s-Non-Sufficit). 
They are currently doing some really cool stuff with persistent modifications on the Orbi!
- Thanks [someonewhocares' Dan Pollock](https://someonewhocares.org/hosts/) for the magnificent hosts file. This project 
wouldn't have been able without it.
- Thanks [Joel Barmettler for teaching me how to upload this to PyPi](https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56)!
- Thanks [PurpleBooth for the README template](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)!

