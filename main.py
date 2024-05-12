from bs4 import BeautifulSoup
import requests
import csv

def find_jobs(html):
    html_text = requests.get(html).text
    #html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords=data+engineer&txtLocation=').text
    #print(html_text)
    soup = BeautifulSoup(html_text,features='lxml')
    jobs = soup.find_all('li',class_="clearfix job-bx wht-shd-bx")
    #print(job)
    list_job = list()
    for job in jobs:
        published_date = job.find('span',class_ = 'sim-posted').text.strip()
        job_dict = dict()
        if published_date == 'Posted few days ago':
            jobs_title = job.find('a').text.strip()
            company_name = job.find('h3',class_ = "joblist-comp-name").text.strip().split('\n')[0]
            skills = [skill.strip() for skill in job.find('span',class_="srp-skills").text.strip().split(',') if skill.strip() != '' ]
            link = job.header.h2.a['href']
            job_dict['title'] = jobs_title
            job_dict['skills'] = skills
            job_dict['company_name'] = company_name
            job_dict['link'] = link
            list_job.append(job_dict)
    return list_job

def saved_jobs(list_job,page):
    page = page
    data = list_job
    field_name = ['title','skills','company_name','link']

    with open(f'data\Job_Post_{page}.csv','w',newline='') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=field_name)
        writer.writeheader()
        writer.writerows(data)
    print(f"Process Saved for Pages : {page}")

def main():
    pages = 10
    for page in range(pages):
        html =  f"https://www.timesjobs.com/candidate/job-search.html?from=submit&luceneResultSize=25&txtKeywords=python&postWeek=60&searchType=personalizedSearch&actualTxtKeywords=python&searchBy=0&rdoOperator=OR&pDate=I&sequence=105&startPage={page}"
        job = find_jobs(html)
        saved_jobs(job,page)

    

if __name__ == '__main__':
    main()
