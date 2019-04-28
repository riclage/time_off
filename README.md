# Time Off Auto Approval

[![Build Status](https://travis-ci.org/riclage/time_off.svg?branch=master)](https://travis-ci.org/riclage/time_off)

A Python script to go through time off requests and auto-approve them. 

Currently supports [BambooHR API](https://www.bamboohr.com/api/documentation/):
> To generate an API key for a given user, users should log in and click their name in the upper right hand corner of any page to get to the user context menu. There will be an "API Keys" option in that menu to go to the page.

## How to use
- Open the `timeoff.py` file and enter the needed values for api keys and contact info
- Check the `model.py/TimeOffRequest` class if you want to modify the auto-approve rules
- Run `timeoff.py`

You may want to setup a cron job to run the script automatically. You also need to create an account with [MailGun](https://www.mailgun.com/) if you want to receive email updates about auto-approvals.

## Updating requirements
We use [pipreqs](https://github.com/bndr/pipreqs) to auto generate the `requirements.txt` file
