#!/usr/local/nagios/libexec/python_web_checks/venv/bin/python3.8

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import subprocess
import os
import argparse

# Set environment variables
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''

my_parser = argparse.ArgumentParser(description='Firefox marionette.')
my_parser.add_argument('-p','--port', action='store', type=str, required=True, help='Marionette listening port.')
my_parser.add_argument('-f','--profile', action='store', type=str, required=False, help='Firefox profile to use.')
args = my_parser.parse_args()

options = FirefoxOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.set_preference("browser.cache.disk.enable", False)
options.set_preference("browser.cache.memory.enable", False)
options.set_preference("browser.cache.offline.enable", False)
options.set_preference("network.http.use-cache", False)

options.set_preference("security.warn_entering_secure", False)
options.set_preference("security.insecure_field_warning.contextual.enabled", False)
options.set_preference("security.certerrors.permanentOverride", True)
options.set_preference("network.stricttransportsecurity.preloadlist", False)
options.set_preference("security.enterprise_roots.enabled", False)

browser_port=args.port
profile_location = args.profile
print(f'usando: {profile_location}')
if profile_location:
    profile = webdriver.FirefoxProfile(profile_location)
else:
    profile = webdriver.FirefoxProfile()
profile.accept_untrusted_certs = True
profile.assume_untrusted_cert_issuer = False

p1 = subprocess.Popen(['netstat', '-ltpn'],stdout=subprocess.PIPE)
p2 = subprocess.Popen(['grep', 'firefox'], stdin=p1.stdout, stdout=subprocess.PIPE)
p3 = subprocess.Popen(['grep', browser_port], stdin=p2.stdout, stdout=subprocess.PIPE)
p4 = subprocess.Popen(['cut', '-f2', '-d:'], stdin=p3.stdout, stdout=subprocess.PIPE)

p1.stdout.close()

output = str(p4.communicate()[0]).split(" ")[0].split("'")[1]

if output != browser_port:
    print('Starting browser...')
    try:
        browser = webdriver.Firefox(firefox_profile=profile, options=options,executable_path='/usr/local/nagios/libexec/python_web_checks/geckodriver',service_log_path='/dev/null',service_args=['--marionette-port',browser_port])
        #browser = webdriver.Firefox(options=options,executable_path='/usr/local/nagios/libexec/python_web_checks/geckodriver',service_log_path='/dev/null',service_args=['--marionette-port',browser_port])
    except Exception as e:
        print(f'Failed to open browser:\n{e}')
        exit(2)
    else:
        browser.delete_all_cookies()
        browser.find_element_by_xpath
        print('Browser opened')
else:
    print(f'Firefox at port {browser_port} found...')

