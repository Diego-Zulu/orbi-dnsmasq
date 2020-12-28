import re
import telnetlib
from getpass import getpass
from time import sleep
import requests

DEBUG_ADDRESS = "http://{}/debug.htm"
USERNAME = "admin"


def telnet_write(tn, _str, wait_until):
    tn.write((_str + "\n").encode('utf-8'))
    telnet_read_until(tn, wait_until)


def telnet_read_until(tn, str_regex):
    regex_list = [str_regex]
    if isinstance(str_regex, list):
        regex_list = str_regex
    tn.expect([re.compile(s.encode('utf-8')) for s in regex_list], timeout=5)


def telnet_into_router(_host, _user, _pass):
    tn = telnetlib.Telnet(_host)

    telnet_read_until(tn, "login: ")
    telnet_write(tn, _user, "Password: ")
    if _pass:
        telnet_write(tn, _pass, "#")
    return tn


def download_hosts_file_into_router(tn, dns_hosts_url):
    print("downloading hosts file")
    telnet_write(tn, "curl %s -k -o /etc/hosts" % dns_hosts_url, "#")


def activate_hosts_file(tn):
    print("removing `no-hosts` from `/etc/dnsmasq.conf`")
    telnet_write(tn, "sed -i 's/no-hosts//g' /etc/dnsmasq.conf", "#")  # Edge case: line not present


def reboot_dns(tn):
    print("killing dnsmasq")
    telnet_write(tn, "kill $(pidof dnsmasq)", "#")
    print("starting dnsmasq")
    telnet_write(
        tn,
        "/usr/sbin/dnsmasq --except-interface=lo -r /tmp/resolv.conf --addn-hosts=/tmp/dhcpd_hostlist",
        "#"
    )

def upload_config_file(tn, file_path):
    with  open(file_path, "r") as f:
        content = f.read()
        print("Applying the following configuration: \n{}".format(content))
        telnet_write(tn, "cat <<EOF > /etc/dnsmasq.conf\n{}\nEOF\n".format(content), "#")
        print("\n new config uploaded")


def get_web_ts(host, username, password):
    r = requests.get(f'http://{host}/debug_detail.htm', auth=(username, password))
    results = re.search('ts="(\d+)', r.text)
    if results:
        print(f"ts={results.group(1)}")
        return results.group(1)
    else:
        raise Exception("ts not found, retry in a minute or two")


def enable_telnet(host, username, password):
    ts = get_web_ts(host, username, password)
    r = requests.post(f'http://{host}/apply.cgi?/debug_detail.htm%20timestamp={ts}', 
                      auth=(username, password),
                      data={'submit_flag':'debug_info', 'hid_telnet':'1', 'enable_telnet':'on'})
    print(f"telnet enable {r.status_code}")
    return r.status_code == 200


def disable_telnet(host, username, password):
    ts = get_web_ts(host, username, password)
    r = requests.post(f'http://{host}/apply.cgi?/debug_detail.htm%20timestamp={ts}', 
                      auth=(username, password),
                      data={'submit_flag':'debug_info', 'hid_telnet':'0'})
    print(f"telnet disable {r.status_code}")
    return r.status_code == 200


def script_main(options, _):
    _pass = options.password
    if _pass is None:
        _pass = getpass('Password: ')
    
    if options.toggle_telnet:
        enable_telnet(options.address, USERNAME, _pass)

    if options.config_file or options.download_hosts:
        tn = telnet_into_router(options.address, USERNAME, _pass)
        if options.config_file:
            upload_config_file(tn, options.config_file)
        if options.download_hosts:
            download_hosts_file_into_router(tn, options.dns_hosts_url)
            activate_hosts_file(tn)
        reboot_dns(tn)
        tn.close()

    if options.toggle_telnet:
        disable_telnet(options.address, USERNAME, _pass)
