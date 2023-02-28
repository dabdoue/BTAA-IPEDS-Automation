# IPEDS Selenium Automation

This repository uses selenium to retrieve data from the IPEDS school database and puts it into a single csv file.

It is run as a basic flask app. Selenium is used on the server to select the requested options from the database, then a csv is downloaded to the server, and that csv is then parsed and filtered, then served to the client. 

Selenium structure is built with future-proofing in mind, with easy functions that allow for easily adding new requested data or making changes based on changes to the database.

Requires pandas, selenium, chromedriver_autoinstaller

To run, simply run `flask run`

To run so that all devices on the same network can access the application, run `flask run --host=0.0.0.0` - this will make the application accessible by going to the server's IP address, then the port of the application (by default 5000). (ex: http://10.192.XX.XXX:5000)
