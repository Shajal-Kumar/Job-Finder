#need to add filtering for more than one unfamiliar skills
from bs4 import BeautifulSoup as bs
import time
import requests as req
from colorama import Fore, Back

search = input(Fore.LIGHTYELLOW_EX + "Which skill do you want to search for: ")
post_time = input(Fore.LIGHTMAGENTA_EX + "How old should the excluded out job posts be (in days): ")
unfamiliar_skill = input(Fore.LIGHTMAGENTA_EX + "Which skill are you unfamiliar with: ")
print(Fore.GREEN + f"Filtering out {post_time} days old posts and posts including {unfamiliar_skill}")

def search_jobs(to_search, time_filter, skill_filter):
    html_text = req.get(f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords={to_search}&txtLocation=").text
    soup = bs(html_text, 'lxml')

    jobs = soup.find_all('li',class_='clearfix job-bx wht-shd-bx')

    for index,job in enumerate(jobs):
        publishing_date = job.find('span', class_='sim-posted').span.text
        if time_filter not in publishing_date:
            company_name = job.find('h3', class_='joblist-comp-name').text.replace(' ','')
            exp = job.find('ul', class_='top-jd-dtl clearfix').li.text.replace('card_travel','')
            loc = job.find('ul', class_='top-jd-dtl clearfix').span.text.replace(' ','')
            skills = job.find('span', class_='srp-skills').text.replace(' ','')
            more_info = job.header.h2.a['href']

            if skill_filter not in skills:
                print()
                print(Fore.LIGHTRED_EX + f"Company Name: {company_name.strip()}\n")
                print(Fore.LIGHTYELLOW_EX + f"Experience Needed: {exp}\n")
                print(Fore.LIGHTYELLOW_EX + f"Location: {loc}\n")
                print(Fore.LIGHTGREEN_EX + f"Skills Needed: {skills.strip()}\n")
                print(Fore.LIGHTWHITE_EX + f"Publishing Date: {publishing_date}\n")
                print(Fore.LIGHTCYAN_EX + f"More Info: {more_info}")
                print('---------------------------------------------')
                with open(f"posts/{index}.txt", 'w') as f:
                    f.writelines([f"Company Name: {company_name.strip()}\n", f"Experience Needed: {exp}\n", f"Location: {loc}\n", f"Skills Needed: {skills.strip()}\n", f"Publishing Date: {publishing_date}\n", f"More Info: {more_info}\n", "---------------------------------------------\n"])

if __name__ == '__main__':
    while True:
        try:
            search_jobs(search, post_time, unfamiliar_skill)
            print(Fore.GREEN + "\n\n......................Waiting for 10 mins......................")
            time.sleep(60)
        except:
            print(Fore.RED + "\nJOBS NOT FOUND!!")
            print(Fore.RED + "\nEXITING THE PROGRAM...............")
            break
