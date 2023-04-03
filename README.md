# Material Checker Support Program

The program purpose is to allow production sites to verify that a figure can read the output from the sticker applicator.

It is still in use, and confirmed that it is needed 03-04-23, due to the project beeing a novelty.

Program was updated to Python3 and still use pygatt for BLE interface.

Sharepoint documentation folder

https://legogroup.sharepoint.com/:f:/r/sites/QTC/Shared%20Documents/QTC-M/49242%20LEAF/Test%20equipment%20for%20LEAF/Figure%20Tester?csf=1&web=1&e=ECXoc1

Direct download of compiled exe (version 0.4)

https://legogroup.sharepoint.com/:u:/s/QTC/EfSEeTDFbFRIsW5tB14f5kUBFohiomc27M4Os_PiDQSn-w?e=2G6T7J


# Install
To perform git clone, first create an access token and run

`git clone https://oauth2:TOKEN@gitlab.legogroup.io/qtc-m/leaf/material-checker.git`

Suggested to use Python 3.9.13 and running it in an environment.
This is needed for support of wx that is used a GUI.

https://github.com/wxFormBuilder/wxFormBuilder

Install from requirements.txt by running

`pip install -r requirements.txt`
