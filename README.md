

# Overview 

The biggest problem to any health problems today is the food we eat and water we drink, because of irregular  diets we find it really difficult to understand what we eat how much is it going to affect us.

Once we put on weight and land up into any health problems we then approach a dietician who takes charges up a hefty price to provide us a diet plan. which again falls on us as how much we follow it.

This brings us to a need to someone tell us what we are eating how much would that cause to our health.

So here we tried to create  an app that is personalised to your needs and your data and tell whats good for your health.

Welcome to SmartDietcian!!!

![Alt text](/images/SmartDiet.png?raw=true)


Smart Dietician is an app that is built to address this particular problem where users can register into it and every-time you wish to eat something just take an image and upload in the app.

The app would tell you how much calories you are going to consume and would that be good for your health considering you’r height, weight and current activity.

This being the MVP version we have just tried to prototype the concept where you just upload a pic and provide how much calories one is going to take in.

Health Monitoring!!!


## Running the app
Install the requirements and setup the development environment.

	make install && make dev

Create the database.

python manage.py initdb

	Run the application.

	python manage.py runserver

Navigate to localhost:5000.

Configuration

The goal is to keep most of the application's configuration in a single file called config.py. I added a config_dev.py and a config_prod.py who inherit from config_common.py. The trick is to symlink either of these to config.py. This is done in by running make dev or make prod.

I have included a working Gmail account to confirm user email addresses and reset user passwords, although in production you should't include the file if you push to GitHub because people can see it. The same goes for API keys, you should keep them secret. You can read more about secret configuration files here.

Read this for information on the possible configuration options.



![Alt text](/images/Health-Monitor.png?raw=true)

Future work
- Integrate with Fit-bit users data to provide Live recommendations 
- Track activities and provide what you should consume now for a better health
- Forecast any health problems 
- What food you should avoid and what food to choose.

Dataset used:

http://www.site.uottawa.ca/~shervin/food/


Note:- The model that is trained is not uploaded in Github as its big model

Contributers
sbelal https://github.com/sbelal/