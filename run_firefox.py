#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import subprocess
import os
import argparse
import re

class PatternNotFoundException(Exception):
    pass

def search_pattern_in_file(file_path, pattern):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                matches = re.findall(pattern, line)
                if matches:
                    #print(f"Pattern '{pattern}' found in the line:")
                    #print(line)
                    #print("Matches:")
                    #for match in matches:
                    #    print(match)
                    regex_pattern = r'user_pref\("marionette\.port", (\d+)\);'
                    matches = re.findall(regex_pattern, line)
                    if matches:
                        number = matches[0]
                        return number
                    else:
                        return "No number found."
            else:
                raise PatternNotFoundException(f"Pattern '{pattern}' not found in the file.")
    except FileNotFoundError:
        return f"File '{file_path}' not found."

if __name__ == "__main__":
        
    # Set environment variables
    os.environ['http_proxy'] = ''
    os.environ['https_proxy'] = ''
    script_path='/home/fernando/Documentos/Projetos/check_website'

    sys_path = os.environ['PATH']
    os.environ['PATH'] = f"{sys_path}:{script_path}:{script_path}/firefox"

    my_parser = argparse.ArgumentParser(description='Firefox marionette.')
    my_parser.add_argument('-p','--profile', action='store', type=str, required=False, help='Firefox profile name.')
    args = my_parser.parse_args()

    if args.profile:
        profile = args.profile
        new_dir_path = f'{script_path}/{profile}' 
        if not os.path.exists(new_dir_path):
            os.makedirs(new_dir_path)
    else:
        new_dir_path = f'{script_path}/profile_default'
        if not os.path.exists(new_dir_path):
            os.makedirs(new_dir_path)
        profile = 'profile_default'

    options = FirefoxOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--profile")
    options.add_argument(f"{script_path}/{profile}")
    options.set_preference("accept_untrusted_certs", True)
    options.set_preference("assume_untrusted_cert_issuer" ,False)
    options.set_preference("browser.cache.disk.enable", False)
    options.set_preference("browser.cache.memory.enable", False)
    options.set_preference("browser.cache.offline.enable", False)
    options.set_preference("network.http.use-cache", False)
    options.set_preference("security.warn_entering_secure", False)
    options.set_preference("security.insecure_field_warning.contextual.enabled", False)
    options.set_preference("security.certerrors.permanentOverride", True)
    options.set_preference("network.stricttransportsecurity.preloadlist", False)
    options.set_preference("security.enterprise_roots.enabled", False)

    try:
        browser_port = search_pattern_in_file(f"{script_path}/{profile}/prefs.js", 'marionette.port')
    except PatternNotFoundException as e:
        print(e)

    #print(browser_port)

    p1 = subprocess.Popen(['netstat', '-ltpn'],stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', 'firefox'], stdin=p1.stdout, stdout=subprocess.PIPE)
    p3 = subprocess.Popen(['grep', browser_port], stdin=p2.stdout, stdout=subprocess.PIPE)
    p4 = subprocess.Popen(['cut', '-f2', '-d:'], stdin=p3.stdout, stdout=subprocess.PIPE)

    p1.stdout.close()

    output = str(p4.communicate()[0]).split(" ")[0].split("'")[1]


    if output != browser_port:
        print('Starting browser...')
        try:
            browser = webdriver.Firefox(options=options)
        except Exception as e:
            print(f'Failed to open browser:\n{e}')
            exit(2)
        else:
            browser.delete_all_cookies()
            print('Browser opened')
    else:
        print(f'Firefox at port {browser_port} found...')

