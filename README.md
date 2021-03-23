# CS162 Web Application

##Project Overview

I have created a Kanban application, with a user login and sign up system. The user has to sign in to see and use the kanban.
If the user enter a username that does not exist in the User database, he will be directed to the sign up page. 

After successfully signing in, the users are able to add to-do tasks and move them to ongoing or done categories 
as they want. All the tasks on the Kanban has an option to be deleted (all 3 categories of tasks can be no longer available
at some point of time). 

Specifically in design, to-do, ongoing, and done are marked with red, blue, and green to show the priorities and nudge
the users to start the to-do tasks. Additionally, I chose to use ordered list to add a timeline to Kanban. For example, if 
the to-do tasks "CS162 Assignment" and "Meal Prep" are moved to done column sequentially, they will have the sequence 
number 1 and 2, respectively, according to their completion order. 

## Run Virtual Environment

Virtual environment is a key component in ensuring that the application is configured in the right environment

##### Requirements
* Python 3
* Pip 3

```bash
brew install python3
```

Pip3 is installed with Python3

##### Installation
To install virtualenv via pip run:
```bash
pip3 install virtualenv
```

## Run Application

Get the application to run:

```bash
python3 -m venv .venv 
source .venv/bin/activate
pip3 install -r requirements.txt
export FLASK_APP=app.py
flask run
```

## Unit Tests
To run the unit tests use the following commands:

```bash
python3 -m test_app
```