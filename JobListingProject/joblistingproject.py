#This project job opportunities from realpython.github.io/fake-jobs/
# I used requests to ==>send HTTP requests to websites ,BeautifulSoup for==>to parse and extract Data from HTML  and Pandas for ==>storing and saving data in CSV format
'''
The pattern of this script goes thus:
1. Send requests to the site
2. Parse HTML wit BeautifulSoup
3. Extract job data (Title, company, salary, location etc)
4. Stores info in a dictionary
5. Convert to Pandas Dataframe
6. Export to CSV file
'''

#We begin by importing the necessary modules
import requests
from bs4 import BeautifulSoup
import pandas as pd

#Our scraping logic begins here
def scrape_jobs(): #Our function accepts no input
    url = "https://realpython.github.io/fake-jobs/"
    response = requests.get(url) #sends request to the website to get the HTML Content

    #Now let's check if the requests was successful
    if response.status_code != 200: #If the request was granted, the status code will be 200
        print("Failed to retrieve request")
        return
    
    #Next, we create an object tjat can parse HTML (Parsing simply means analysing the HTML and dividing it into simple components)
    soup_job = BeautifulSoup(response.text, "html.parser") #html.parser tells it to use the built-in parser
    
    # Next, we find all the job cards on the page stored in "div". They have also the class content stored in class.
    #This can be checked by using Developer tools in the browser page
    job_elements = soup_job.find_all("div", class_="card-content")
    
    jobs_data = [] #Empty list to store all the job data we just scraped

    #Looping throught the job data to pick out the interesting/needed info
    for job_elem in job_elements:
        title = job_elem.find("h2", class_="title").text.strip() #Picking out the job title
        company = job_elem.find("h3", class_="company").text.strip() #Picking out the Company offering the job
        location = job_elem.find("p", class_="location").text.strip() #Picking out the location where the job is
        link = job_elem.find_all("a")[-1]["href"]  # Last link is the "Apply" link
        
        #Appending them to the empty list created already
        jobs_data.append({
            "Title": title,
            "Company": company,
            "Location": location,
            "Apply Link": link
        })

    # Save to CSV
    df = pd.DataFrame(jobs_data) #Converting the list of jobs into Pandas DataFrame model which is easy to work with
    df.to_csv("fake_jobs.csv", index=False) #Saving to a file named fake_jobs.csv and not adding the index
    print("Jobs successfully saved to fake_jobs.csv!")

scrape_jobs()
