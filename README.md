# Simple Signup Form with Docker
This Python sample application uses the [Flask](http://flask.pocoo.org/) framework and [Bootstrap](http://getbootstrap.com/) to build a simple, scalable customer signup form that is deployed to [AWS Elastic Beanstalk](http://aws.amazon.com/elasticbeanstalk/). The application stores data in [Amazon DynamoDB](http://aws.amazon.com/dynamodb/) and publishes notifications to the [Amazon Simple Notification Service (SNS)](http://aws.amazon.com/sns/) when a customer fills out the form.

This version of the application has been modified so it can be packaged and deployed as a Docker container. 

## The Docker Parts
Packaging this Python application with Docker required us to add two files:

1. `Dockerfile` - Elastic Beanstalk uses Docker on each of your EC2 Instances to build the Docker Image described by this file:

        FROM ubuntu:12.10

        # Install Python Setuptools
        RUN apt-get install -y python-setuptools

        # Install pip
        RUN easy_install pip

        # Add and install Python modules
        ADD requirements.txt /src/requirements.txt
        RUN cd /src; pip install -r requirements.txt

        # Bundle app source
        ADD . /src

        # Expose
        EXPOSE  5000

        # Run
        CMD ["python", "/src/application.py"]
        
2. `Dockerrun.aws.json` - This file describes how to run the Docker Image created by the `Dockerfile`. It indicates that `/var/app` on the EC2 Instance should be mapped to `/var/app` on the Docker container, and instructs Elastic Beanstalk to copy log files from `/var/eb_log` on the container to S3:

        {
          "AWSEBDockerrunVersion": "1",
          "Volumes": [
            {
              "ContainerDirectory": "/var/app",
              "HostDirectory": "/var/app"
            }
          ],
          "Logging": "/var/eb_log"
        }
        
## Instructional Videos
This app includes a quick 3-part video series on YouTube that will walk you through deploying, using, and customizing the application in 10 minutes or less.

### An Important Note About Part 1
The **Part 1** video below describes how to deploy the non-Docker version of this application. To deploy this Dockerized sample, do two things:

* Download the Docker-specific ZIP file from the Releases page described in the video.
* Choose 'Docker' instead of 'Python' in the 'Environment Type' step of the wizard. 

---

1. [Part 1: http://youtu.be/rsg4YI4mljg](http://youtu.be/rsg4YI4mljg)
2. [Part 2: http://youtu.be/IuwfVX52PV8](http://youtu.be/IuwfVX52PV8)
3. [Part 3: http://youtu.be/DrRr-JgdgzE](http://youtu.be/DrRr-JgdgzE)

## Features

### Themes
The code includes several Bootstrap themes from [bootswatch.com](http://bootswatch.com/). You can dynamically change the active theme by setting the THEME environment variable in the [Elastic Beanstalk Management Console](https://console.aws.amazon.com/elasticbeanstalk):

![](misc/theme-flow.png)

Installed themes include:

* [amelia](http://bootswatch.com/amelia)
* [default](http://bootswatch.com/default)
* [flatly](http://bootswatch.com/flatly)
* [slate](http://bootswatch.com/slate)
* [united](http://bootswatch.com/united)

### Flask Debugging
Similar to themes, you can control Flask debugging by toggling the FLASK_DEBUG env var from the [Elastic Beanstalk Management Console](https://console.aws.amazon.com/elasticbeanstalk).