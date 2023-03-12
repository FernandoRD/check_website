# check_website

 Nagios script that interact to a website to check if it´s OK

## Pre requisites:

### System:

1 - Firefox browser "https://www.mozilla.org/en-US/firefox/all/#product-desktop-release"
 
2 - Geckodriver compatible with installed firefox "https://github.com/mozilla/geckodriver"

3 - Compatibility table "https://firefox-source-docs.mozilla.org/testing/geckodriver/Support.html"

 ### Python:

A venv with selenium webdriver_manager marionette-driver marionette modules installed.

## Running the script

The script works in two parts.
 
The run_firefox is responsable to keep a firefox instance open and running for use.

```shell
 ./run_firefox -p port [Mandatory] -f profile [Optional]
```

Then you may put it to run in crontab or even create a service in Nagios to check if any firefox instance is running at the given port.

Then run the check:

```shell
 ./check_website.py -u http://www.foobar.com -w 5 -c 10 -e module_to_execute -p port
```

It will use the firefox running at the given port to make the check and then returns the time spent in case of success.

The module_to_execute is a python script that is imported as a module and executed. It should contain the step by step interaction writen in it

There is an file called search_google.py for an example.
