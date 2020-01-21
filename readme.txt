INSTRUCTIONS:
Install python 3.7.3 , make sure you have checked 'install to path' option
Install MySQL database server preferably version  5.7 to avoid issues
Navigate to the current folder root and fire up your command line or terminal
Run the command 'pip install -r requirements.txt'
Make sure you have internet connection and allow the process to finish
open your mysql server and create a database 'ic_loans'
Navigate to the folder 'ic_loans' and open the settings.py file using a text editor of your choice
Scroll down to the databases section and make the following changes
Next to the 'USER' key change it to your database username
Next to the 'PASSWORD' key change it to your password  for MySQL database
if you are running on  different port other than 3306 for mysql or host , you need to specify that too next to the "HOST and "PORT" key
Open mysql server and run data migration import wizard from the data.sql file on the folder root.
Now go back to the root directory 
In the terminal , run the command 'python manage.py migrate' to make migrations to the database
In the terminal , run the command 'python manage.py runserver' to start the server 
if all is well there should be no errors and you should access the system from address "http://127.0.0.1:8000" on your browser
Enjoy yourself!!


ASSUMPTIONS:
That you are running on a windows version preferably windows 10.
That you have basic skills for command line navigation and MySQL administration.
That you are running from a localhost environment not from a live production setup.



Tools Used:
Note that this is a python/django web application running on a MySQL database
You can use any text editor as you wish


PRECAUTIONS:
Note that you dont need to reupload the excel data 
it is quite a huge process and takes up to around 45 mins to fully add the 80,913 records to the database.



Author:
Name: KEN MURIITHI
EMAIL: muriithiken0@gmail.com
PHONE: 254701416600

