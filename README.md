# orbi-dnsmasq
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

[![PyPI version](https://badge.fury.io/py/orbi-dnsmasq.svg)](https://badge.fury.io/py/orbi-dnsmasq)

Python command to set a hosted hosts file as dnsmasq on your orbi router.

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
- Downloads hosts file (you can specify a custom url with the `-d` flag, or check the default one I'm using 
on [someonewhocares.org](https://someonewhocares.org/hosts/)).
- Deletes the `no-hosts` line to active dnsmasq.
- Reboots Orbi's dns.
- Turns off telnet  on the debug Orbi GUI if `-t` flag was supplied.

## Getting Started

### Prerequisites

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

I don't like leaving my telnet port open when I'm not using it, so I built in feature with selenium to toggle this option 
on before running configs on the Orbi, and turning it off afterwards. If you want to use this feature, you'll first need to 
[download one of the selenium webdrivers](https://selenium-python.readthedocs.io/installation.html#introduction).
Any will do, just make sure you also have that browser installed on your system.

After that, run:

```
orbi-dnsmasq -t -w path/to/downloaded/webdriver
```

You can avoid the `-w` flag if you put the downloaded webdriver in your PATH.

## Possible things to add:

- Read password from ENV var, don't ask it if already found.
- Flag option to set username to connect with, use admin as default (is this even necessary?).
- Create Telnet object with telnet_write methods, cleaning up the code.
- Flag option to indicate how much to wait for web elements to appear, and to indicate polling rate.
- Use polling rate and selenium with expected condition wait.
- Remove selenium's send keys TODO and `keyboard` dependency when [this issue is fixed](https://github.com/w3c/webdriver/issues/385).
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


## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/nferro"><img src="https://avatars1.githubusercontent.com/u/2065319?v=4" width="100px;" alt=""/><br /><sub><b>Nuno Ferro</b></sub></a><br /><a href="https://github.com/Diego-Zulu/orbi-dnsmasq/commits?author=nferro" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!