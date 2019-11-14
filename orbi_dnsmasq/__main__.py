from optparse import OptionParser
from orbi_dnsmasq.orbi_dnsmasq import script_main

DEFAULT_DNS_HOSTS_FILE = "https://someonewhocares.org/hosts/hosts"

parser = OptionParser()
parser.add_option(
    "-d",
    "--dns-hosts",
    action="store",
    default=DEFAULT_DNS_HOSTS_FILE,
    dest="dns_hosts_url",
    help="Url to download dns-hosts file",
    type="string"
)
parser.add_option(
    "-t",
    "--toggle",
    action="store_true",
    dest="toggle_telnet",
    help="Toggle telnet service on the orbi debug site with selenium"
)
parser.add_option(
    "-w",
    "--webdriver",
    action="store",
    default=None,
    dest="webdriver_path",
    help="Path to the webdriver for selenium",
    type="string"
)


def command_line_main():
    (param_options, args) = parser.parse_args()
    script_main(param_options, args)

if __name__ == "__main__":
    command_line_main()
