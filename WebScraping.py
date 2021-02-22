import requests
import csv
from bs4 import BeautifulSoup
from itertools import zip_longest

job_title = []
company_name = []
location = []
skills = []
links = []
salary = []
job_requirment =[]
date =[]
page_num =0

while True:
    # fetch the url 
    result = requests.get(f"https://wuzzuf.net/search/jobs/?a=spbg&q=python&start={page_num}")

    # save page content 
    src = result.content

    # creat soup object to parse content
    soup = BeautifulSoup(src , "lxml")

    page_limit = int(soup.find("strong").text)
    if (page_num > page_limit // 15):
        print("Finish")
        break

    # containing info we need 
    # job titles, company names, location, job skills
    job_titles = soup.find_all("h2" , {"class": "css-m604qf"})
    company_names = soup.find_all("a", {"class":"css-17s97q8"})
    locations = soup.find_all("span", {"class":"css-5wys0k"})
    job_skills = soup.find_all("div" , {"class":"css-1w0948b"})
    posted_new = soup.find_all("div" , {"class":"css-4c4ojb"})
    posted_old = soup.find_all("div" , {"class":"css-do6t5g"})
    posted =[*posted_new, *posted_old]


    # put infoo in lists 
    for i in range(len(job_titles)):
        job_title.append(job_titles[i].text)
        links.append(job_titles[i].find("a").attrs["href"])
        company_name.append(company_names[i].text)
        location.append(locations[i].text)
        skills.append(job_skills[i].text)
        Date_text= posted[i].text.replace("-","").strip()
        date.append(Date_text)

    page_num +=1
    

# enter another page 
for link in links:
    result = requests.get(link)
    src = result.content
    soup = BeautifulSoup(src , "lxml")
    salaries = soup.find("div", {"class":"matching-requirement-icon-container" , "data-toggle":"tooltip" ,"data-placement":"top"})
    salary.append(salaries.text.strip())
    job_requirments = soup.find("span" , {"itemprop":"responsibilities"}).ul
    requirment_text=""
    for i in job_requirments.find_all("li"):
        requirment_text += i.text +"| "
    requirment_text = requirment_text[:-2]
    job_requirment.append(requirment_text)

# print(job_requirment)
    

# create csv file and fill it
File_List = [job_title, company_name, date, location , skills , links , salary , job_requirment]
Beshbesh = zip_longest(*File_List)
with open ("D:\Projects\WebScript\job.csv" , "w") as myfile:
    wr = csv.writer(myfile)
    wr.writerow(["Job title" , "Company name" , "Job posted" ,"Location" , "Skills" , "Links" ,"Salary" ,"Job requirments"])
    wr.writerows(Beshbesh)






