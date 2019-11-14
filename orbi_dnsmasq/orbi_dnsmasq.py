import keyboard
import re
import telnetlib
from getpass import getpass
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from time import sleep

DEBUG_HOST = "https://orbilogin.com/debug.htm"
TELNET_HOST = "orbilogin.com"
USERNAME = "admin"


def ask_for_credentials():
    _pass = getpass('Password: ')
    return USERNAME, _pass


def enter_orbi_debug_credentials(_user, _pass, driver):
    user_pass_alert = driver.switch_to.alert

    for word in [_user, _pass]:
        keyboard.write(word)  # TODO: Use selenium's send keys when fixed for alerts
        keyboard.press_and_release("tab")
    user_pass_alert.accept()


def get_telnet_checkbox(driver):
    form_frame_array = []
    while len(form_frame_array) == 0:
        sleep(1)
        form_frame_array = driver.find_elements_by_id("formframe")
    driver.switch_to.frame(form_frame_array.pop())

    telnet_array = []
    while len(telnet_array) == 0:
        sleep(1)
        telnet_array = driver.find_elements_by_name("enable_telnet")

    return telnet_array.pop()


def change_telnet_status(status, checkbox):
    if status == (checkbox.get_attribute('checked') is None):
        checkbox.click()


def set_orbi_telnet(status, driver):
    telnet_checkbox = get_telnet_checkbox(driver)
    change_telnet_status(status, telnet_checkbox)


def telnet_write(tn, _str, wait_until):
    tn.write((_str + "\n").encode('utf-8'))
    telnet_read_until(tn, wait_until)


def telnet_read_until(tn, str_regex):
    regex_list = [str_regex]
    if isinstance(str_regex, list):
        regex_list = str_regex
    tn.expect([re.compile(s.encode('utf-8')) for s in regex_list])


def telnet_into_router(_user, _pass):
    tn = telnetlib.Telnet(TELNET_HOST)

    telnet_read_until(tn, "login: ")
    telnet_write(tn, _user, "Password: ")
    if _pass:
        telnet_write(tn, _pass, "#")
    return tn


def go_into_etc(tn):
    telnet_write(tn, "cd etc", "#")


def download_hosts_file_into_router(tn, dns_hosts_url):
    telnet_write(tn, "curl %s -k -o hosts" % dns_hosts_url, "#")


def activate_hosts_file(tn):
    telnet_write(tn, "vim dnsmasq.conf", "- dnsmasq.conf")
    telnet_write(tn, ":%s/no-hosts//e", ["- dnsmasq.conf", "Put"])  # Edge case: line not present
    telnet_write(tn, ":wq", "#")


def reboot_dns(tn):
    telnet_write(tn, "kill $(pidof dnsmasq)", "#")
    telnet_write(
        tn,
        "/usr/sbin/dnsmasq --except-interface=lo -r /tmp/resolv.conf --addn-hosts=/tmp/dhcpd_hostlist",
        "#"
    )


def find_selenium_driver(webdriver_path):
    possible_drivers = [
        webdriver.Chrome,
        webdriver.Edge,
        webdriver.Firefox,
        webdriver.Safari
    ]
    for driver in possible_drivers:
        try:
            if webdriver_path:
                return driver(webdriver_path)
            else:
                return driver()
        except WebDriverException:
            continue
    raise IOError('No selenium web driver was found')


def script_main(options, _):
    _user, _pass = ask_for_credentials()
    driver = None

    if options.toggle_telnet:
        driver = find_selenium_driver(options.webdriver_path)
        driver.get(DEBUG_HOST)
        enter_orbi_debug_credentials(_user, _pass, driver)
        set_orbi_telnet(True, driver)

    tn = telnet_into_router(_user, _pass)
    go_into_etc(tn)
    download_hosts_file_into_router(tn, options.dns_hosts_url)
    activate_hosts_file(tn)
    reboot_dns(tn)
    tn.close()

    if options.toggle_telnet:
        driver.get(DEBUG_HOST)
        set_orbi_telnet(False, driver)
        driver.quit()
