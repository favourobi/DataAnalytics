# I keep improving the job scraping code whenever my friends give me a suggestion to add. 
# This time around, I am including a search history feature
# I will be creating a .txt file to save searches and will show anyone that wants to use my code the 5 most recent searches
# Libraries used: requests, bs4, tabulate, datetime, os, termcolor
# I will try my best to use enough comments to explain everything that was done here
# Wish me luck. Ciao! 

# Import required libraries
import requests                          # For making HTTP requests
from bs4 import BeautifulSoup            # For parsing HTML content
from tabulate import tabulate            # For displaying data in a table format
from termcolor import colored            # For coloring keyword text in terminal
import os                                # For file and path operations
from datetime import datetime            # For adding timestamps to history

# Start with a File name for saving search history
HISTORY_FILE = "search_history.txt"

# Create a Function to display the last few search entries from history
def show_search_history(limit=5):
    # Check if the history file exists
    if os.path.exists(HISTORY_FILE):
        print("\n Last Searches:\n")
        # Open and read the file
        with open(HISTORY_FILE, "r") as file:
            lines = file.readlines()
            # Show only the last `limit` lines (default 5)
            last_lines = lines[-limit:]
            for entry in last_lines:
                print("• " + entry.strip())  # Print each entry
        print()

# Function to save a new search log to the history file
def log_search(keyword, location, company, count):
    with open(HISTORY_FILE, "a") as file:
        # Get the current time
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        # Format the entry
        entry = f"[{timestamp}] keyword='{keyword}', location='{location}', company='{company}', matches={count}\n"
        # Append it to the file
        file.write(entry)

# Main function to scrape jobs and apply filtering + formatting
def scrape_filtered_jobs():
    # Show previous searches before starting new one
    show_search_history()

    # Ask user for filters
    keyword = input("Enter a job keyword to search for (e.g. python, data): ").lower().strip()
    location_filter = input("Filter by location (or leave blank to skip): ").lower().strip()
    company_filter = input("Filter by company (or leave blank to skip): ").lower().strip()

    # URL of the fake job listing page
    url = "https://realpython.github.io/fake-jobs/"
    response = requests.get(url)

    # If the website doesn't respond properly
    if response.status_code != 200:
        print("Failed to retrieve the web page.")
        return

    # Parse the HTML response
    soup_job = BeautifulSoup(response.text, "html.parser")
    job_elements = soup_job.find_all("div", class_="card-content")  # Get all job cards

    job_rows = []  # This will store matching job results

    # Loop through each job listing
    for job_elem in job_elements:
        # Extract job info
        title = job_elem.find("h2", class_="title").text.strip()
        company = job_elem.find("h3", class_="company").text.strip()
        location = job_elem.find("p", class_="location").text.strip()
        link = job_elem.find_all("a")[-1]["href"]  # Get the "Apply" link

        # Filtering conditions
        if keyword not in title.lower():
            continue  # Skip if keyword not in job title
        if location_filter and location_filter not in location.lower():
            continue  # Skip if location doesn't match
        if company_filter and company_filter not in company.lower():
            continue  # Skip if company doesn't match

        # Highlight keyword in title
        highlight = lambda word: colored(word, "yellow", attrs=["bold"])
        # Replace the keyword with highlighted version (only works for first match)
        highlighted_title = title.replace(keyword, highlight(keyword)) if keyword in title.lower() else title

        # Add this job to the table rows
        job_rows.append([highlighted_title, company, location, link])

    # Save the search into history with number of matches
    match_count = len(job_rows)
    log_search(keyword, location_filter or "-", company_filter or "-", match_count)

    # Display results in table format
    if job_rows:
        print("\n" + tabulate(
            job_rows,
            headers=["Job Title", "Company", "Location", "Apply Link"],
            tablefmt="fancy_grid"
        ))
        print(f"\n Total matches found: {match_count}")
    else:
        print(f"\n No matching jobs found with the given filters.")

# Run the script
scrape_filtered_jobs()
