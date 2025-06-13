# I have added a dashboard to the code
# You would need to add streamlit to achieve this. You can use pip install streamlit
# Run the code using streamlit run 'filename'. Make sure you are in the correct folder using cd 'Directory_name'

import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime

HISTORY_FILE = "search_history.txt"  # File to log history


# Show previous searches
def show_search_history(limit=5):
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            lines = file.readlines()[-limit:]
            st.subheader(" Last Searches")
            for line in lines:
                st.markdown(f"- {line.strip()}")
    else:
        st.info("No search history found.")


# Log new search to file
def log_search(keyword, location, company, count):
    with open(HISTORY_FILE, "a") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = f"[{timestamp}] keyword='{keyword}', location='{location}', company='{company}', matches={count}\n"
        file.write(entry)


# Clear search history
def clear_search_history():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
        st.success(" Search history cleared.")
    else:
        st.warning("No history to clear.")


# Main scraping logic
def scrape_jobs(keyword, location_filter, company_filter):
    url = "https://realpython.github.io/fake-jobs/"
    response = requests.get(url)

    if response.status_code != 200:
        st.error("Failed to retrieve job listings.")
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, "html.parser")
    jobs = []

    job_cards = soup.find_all("div", class_="card-content")
    for job_elem in job_cards:
        title = job_elem.find("h2", class_="title").text.strip()
        company = job_elem.find("h3", class_="company").text.strip()
        location = job_elem.find("p", class_="location").text.strip()
        link = job_elem.find_all("a")[-1]["href"]

        # Apply filters
        if keyword and keyword not in title.lower():
            continue
        if location_filter and location_filter not in location.lower():
            continue
        if company_filter and company_filter not in company.lower():
            continue

        jobs.append({
            "Job Title": title,
            "Company": company,
            "Location": location,
            "Apply Link": link
        })

    return pd.DataFrame(jobs)


# Streamlit Dashboard UI
st.set_page_config(page_title="Job Search Dashboard", layout="centered")
st.title(" Python Job Search Dashboard")

with st.sidebar:
    st.header(" Filters")
    keyword = st.text_input("Keyword", placeholder="e.g. python, data").lower().strip()
    location = st.text_input("Location", placeholder="e.g. remote, lagos").lower().strip()
    company = st.text_input("Company", placeholder="e.g. google").lower().strip()

    if st.button(" Search Jobs"):
        results = scrape_jobs(keyword, location, company)
        log_search(keyword or "-", location or "-", company or "-", len(results))

        st.session_state["results"] = results

    if st.button(" Clear Search History"):
        clear_search_history()

# Display results
if "results" in st.session_state and not st.session_state["results"].empty:
    st.subheader(f" Found {len(st.session_state['results'])} job(s)")
    st.dataframe(st.session_state["results"], use_container_width=True)
elif "results" in st.session_state:
    st.warning(" No matching jobs found.")

# Show history
show_search_history()
