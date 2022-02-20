#Deriving the latest base image
FROM python:latest

#Labels as key value pair
LABEL Maintainer="mohit.sharma"

# Any working directory can be chosen as per choice like '/' or '/home' etc
# i have chosen /usr/app/src
WORKDIR /usr/app/src

RUN pip install google.cloud
RUN pip install --upgrade google-cloud-storage

#to COPY the remote file at working directory in container
COPY webscrapping.py ./
# Now the structure looks like this '/usr/app/src/webscrapping.py'

#CMD instruction should be used to run the software
#contained by your image, along with any arguments.

#Using unbuffered option <-u> so that the output of python script is visible in docker logs
CMD [ "python", "-u", "./webscrapping.py"]


