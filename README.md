# Software Engineering Project - Team 38

Software Engineering Project - Team 38
Designing an E-Scooter web application

## Description
Our project implements a solution for an e-scooter rental service. This project runs the service on a website where a customer can view the availability of scooters at various locations around leeds. Once a locations is chosen the customer can enter their payment details and then recieve a cofirmation email for their order. If a customer is not logged in they have the option to sign up. Once they are logged in they can also view their order history. Any customer can also submit an issue to be viewed by an employee/admin.

Staff/admin can login using special login details. Staff has the ability to view and escalate the priority of reports submitted by customers as well as make bookings for unregistered users.
Admins can view higher priority issues.
Admim has the ability to manage a scooters location availability as well as add new scooters to the system. The admin can also view the revenue for the past few weeks as well as what hiring option has made the most money in the past week. Higher priority reports can also be viewed by the admin.
The admin can also change the pricing of each of the time options.
The admin login details are email: admin@admin.com password: Password1
The staff login details are email: staff@staff.com password: Password1

## Installation
First make a folder and create a python virtual environment by first going into the path of the folder where the enviroment should reside usimg smd and entering the following command:
"python -m venev env"

Once that is done download the repository in to a seprate folder and place it next to the enviromnent
Then type in "env\Scripts\activate" using cmd and pip install our packages using "pip install -r req.txt" The req.txt file can be found in our repository.
Now to run the program type "python run.py" while in the folder containing the project. This should launch the server. Then use the provided ip to enter the website. "python test.py"
can be used to run our unit tests

## Requiements
-python 3.10  
-pip is installed  
-req.txt

## Authors and acknowledgment
Krzysztof Kamola,
Safwan Chowdhury,
Tamir Cohen,
Maverick Low,
Adam Zbikowski and
Kevin Braszkiewicz.
