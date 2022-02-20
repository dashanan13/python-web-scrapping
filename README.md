# **Python Webscrapping project**

***This project is intended to showcase python capabilities to scrape websites with native functions***

## **Background**

In order to extract information from a Webpage it is important ot check fhow information is structured on the page.
It is possible to check the HTML of the page by opening it in chrome or edge browser, right click on it and select "inspect".
This opens a new sub window that can give you an idea about what tags have informatino you need.

## **How to use the code**
###### 1. Execute it natively on a local machine or a virtual machine:
    - Pre requsites: Python3
    - Install the required libraries, to upload files to GCP via: 
        - pip install google.cloud
        - pip install --upgrade google-cloud-storage
    - Clone this repository
    - Change directory to the repository folder
    - Execute: python3 webscrapping.py

###### 2. Execute it as a Docker container:
    - Pre requsites: Python3 and Docker
    - Clone this repository
    - Change directory to the repository folder
    - Create an Image out of Docker file: docker build -t webscrapping:1.0 ./PythonDemo/python-web-scrapping
    - Execute the container based on the image
        - Crash and burn container, attached: docker run -it --rm --name=webscrap webscrapping:1.0
        - Crash and burn container, detached: docker run -d --rm --name=webscrap webscrapping:1.0
        - Normal container, attached: docker run -it --name=webscrap webscrapping:1.0

## Notes: 
The public bucket used in the code has been deleted, please use your own bucket.
