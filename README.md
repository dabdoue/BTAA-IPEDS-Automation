# IPEDS Selenium Automation

This repository uses selenium to retrieve data from the IPEDS school database and puts it into a single csv file.

It is run as a basic flask app. Selenium is used on the server to select the requested options from the database, then a csv is downloaded to the server, and that csv is then parsed and filtered, then served to the client. 

Selenium structure is built with future-proofing in mind, with easy functions that allow for easily adding new requested data or making changes based on changes to the database.

Requires pandas, selenium, chromedriver_autoinstaller

Run with `flask run`
