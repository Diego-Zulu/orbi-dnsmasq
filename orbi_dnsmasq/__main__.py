from optparse import OptionParser
from orbi_dnsmasq.orbi_dnsmasq import script_main

DEFAULT_DNS_HOSTS_FILE = "https://someonewhocares.org/hosts/hosts"

parser = OptionParser()
parser.add_option(
    "-d",
    "--dns-hosts",
    action="store_true",
    default=False,
    dest="download_hosts",
    help="Download dns-hosts file"
)
parser.add_option(
    "-u",
    "--dns-url",
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
    "-a",
    "--address",
    action="store",
    default="orbilogin.com",
    dest="address",
    help="IP or hostname of your router",
    type="string"
)
parser.add_option(
    "-p",
    "--password",
    action="store",
    default=None,
    dest="password",
    help="The password for the admin user (warning: insecure, watch out for your terminal's history)",
    type="string"
)
parser.add_option(
    "-c",
    "--config-file",
    action="store",
    dest="config_file",
    help="Path to config file to override default Orbi file"
)


def command_line_main():
    (param_options, args) = parser.parse_args()
    script_main(param_options, args)

if __name__ == "__main__":
    command_line_main()
