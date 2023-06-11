#!/usr/bin/python3

# Debian:
# python3 -m pip install --upgrade pip
# pip3 install selenium webdriver_manager marionette-driver marionette
# apt install libgtk-3-0 libdbus-glib-1-dev libx11-xcb1

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re

import time
import os
import argparse
from marionette_driver import marionette

class PatternNotFoundException(Exception):
    pass
class InstanceNotFoundException(Exception):
    pass

def search_pattern_in_file(file_path, pattern, profile):
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
                        raise InstanceNotFoundException(f"Firefox instance for profile {profile} not found in the file.")
            else:
                raise PatternNotFoundException(f"Pattern '{pattern}' not found in the file.")
    except FileNotFoundError:
        return f"File '{file_path}' not found."

if __name__ == "__main__":

    # Set environment variables
    os.environ['http_proxy'] = ''
    os.environ['https_proxy'] = ''
    script_path='/home/fernando/check_website'

    my_parser = argparse.ArgumentParser(description='Check Website.', epilog='Created by Fernando Durso, GitHub: FernandoRD')
    my_parser.add_argument('-u','--url', action='store', type=str, required=True, help='Link/url')
    my_parser.add_argument('-s','--screenshot', action='store_true', help='PNG Screenshot.')
    my_parser.add_argument('-w','--warning', action='store', type=int, required=True, help='WARNING Threshold')
    my_parser.add_argument('-c','--critical', action='store', type=int, required=True, help='CRITICAL Threshold')
    my_parser.add_argument('-e','--exec', action='store', type=str, required=True, help='Python script to import & execute')
    my_parser.add_argument('-p','--profile', action='store', type=str, required=True, help='Firefox profile of desired instance to use')

    args = my_parser.parse_args()

    SITE=args.url
    profile=args.profile
    PRINTP=args.screenshot
    WARNING=args.warning
    CRITICAL=args.critical
    exec_script = args.exec

    try:
        browser_port = search_pattern_in_file(f"{script_path}/{profile}/prefs.js", 'marionette.port', profile)
    except PatternNotFoundException or InstanceNotFoundException as e:
        print(e)

    # Instantiate the Marionette (client) class
    try:
        browser = marionette.Marionette(host='localhost', port=browser_port)
    except Exception as e:
        print(e)
        exit(2)

    browser.start_session()

    # Clean all browser open windows or tabs before proceed
    for i in browser.window_handles:
        if len(browser.window_handles) > 1:
            print('Atual Deletando: ' + browser.current_window_handle)
            print(browser.close())
            browser.start_session()
            
    start_time=time.time()
    delay = 3

    # Import a module with its name passed as argument
    # The module will have one function called navigate that do the interaction with the site
    # In this way, just need a .py for each site e pass it as parameter (without the .py extension)
    exec_module = __import__(exec_script)

    exec_module.navigate(browser, SITE, PRINTP, delay, script_path)

    total_time=time.time() - start_time

    if total_time < WARNING:
        print("OK: {} - Execution time: {:.2f} s | exec_time={:.2f}s;{};{};0;{}".format(exec_script, total_time, total_time, WARNING, CRITICAL,CRITICAL*2))
        exit(0)
    elif total_time > WARNING and total_time < CRITICAL:
        print("WARNING: {} - Execution time: {:.2f} s | exec_time={:.2f}s;{};{};0;{}".format(exec_script, total_time, total_time, WARNING, CRITICAL,CRITICAL*2))
        exit(1)
    elif total_time > CRITICAL:
        print("CRITICAL: {} - Execution time: {:.2f} s | exec_time={:.2f}s;{};{};0;{}".format(exec_script, total_time, total_time, WARNING, CRITICAL,CRITICAL*2))
        exit(2)
