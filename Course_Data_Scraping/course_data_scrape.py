from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from path import DRIVER_PATH, COURSE_DATA_PATH
from bs4 import BeautifulSoup
import json
import re
import datetime
import os

driver_path = DRIVER_PATH

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options, executable_path=driver_path)

driver.get('https://www.montgomerycollege.edu/admissions-registration/search-the-class-schedule.html')
# Use html from selenium page to create BS4 soup
html = driver.page_source
soup = BeautifulSoup(html, "lxml")

class_list_codes = []
for x in soup.find_all("span", class_="class-list-code"):
    class_list_codes.append(x.text)

# class_list_codes = ['ACCT', 'CMSC', 'NURS']
for x in class_list_codes:

    driver.get('https://appserv.montgomerycollege.edu/courselistblock_test/RedirectToSSB.aspx?term_in=202110&sel_subj=' + x + '&sel_camp=&sel_levl=&sel_attr=')

    # Use html from selenium page to create BS4 soup
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")

    class_names = soup.find_all("table", class_="datadisplaytable", summary="This layout table is used to present the sections found")
    class_contents = soup.find_all("table", class_="datadisplaytable", summary="This table lists the scheduled meeting times and assigned instructors for this class..")

    data = {}

    for n in class_names:
        name = n.find('b').text
        data[name] = []

    for c in class_contents:
        course_info = c.find_all("td", class_="dddefault")

        # Get data from table
        course = course_info[0].text
        crn = course_info[1].text
        credits = course_info[2].text
        days = course_info[3].text
        time = course_info[4].text
        dates = course_info[5].text
        seats = course_info[6].text
        waitlist = course_info[7].text
        campus = course_info[8].text
        location = course_info[9].text
        instructor = course_info[10].text
        schedule_type = course_info[11].text

        # Processing data

        # Course name (split letters and numbers)
        index = re.search("\d", course).start()
        course = course[:index] + ' ' + course[index:]

        # Credits
        credits = re.sub("\s", "", credits)

        # Class days
        class_days = {
            'monday' : bool(re.search("M", days)),
            'tuesday' : bool(re.search("T", days)),
            'wednesday' : bool(re.search("W", days)),
            'thursday' : bool(re.search("R", days)),
            'friday' : bool(re.search("F", days)),
            'saturday' : bool(re.search("S", days)),
            'sunday' : bool(re.search("U", days))
        }

        # Class times
        tba = bool(re.search("TBA", time))
        start_time = ""
        end_time = ""
        if not tba: 
            time = re.sub("m", "M", time)
            time = re.sub("p", "P", time)
            time = re.sub("a", "A", time)
            time = re.sub("\s", "", time)
            times = re.split("-", time)
            start_time = times[0]
            end_time = times[1]
            start_time = datetime.datetime.strptime(start_time, '%I:%M%p')
            end_time = datetime.datetime.strptime(end_time, '%I:%M%p')

        class_times = {
            'start' : str(start_time),
            'end' : str(end_time),
            'tba' : tba
        }

        print("Retrieving: " + course + " " + crn + " " + credits + " " + days + " " + time + " " + seats + " " + waitlist + " " + campus + " " + location + " " + instructor + " " + schedule_type)

        # Adding class info to data hash
        for h in data:
            temp = course + "$"
            if bool(re.search(temp, h)):
                data[h].append({
                    'course' : course,
                    'crn' : crn,
                    'credits' : credits,
                    'days' : class_days,
                    'times' : class_times,
                    'seats' : seats,
                    'waitlist' : waitlist,
                    'campus' : campus,
                    'location' : location,
                    'instructor' : instructor,
                    'schedule_type' : schedule_type
                })
                break

    # Remove old file if it exists
    try: 
        os.remove(COURSE_DATA_PATH + x + '.txt')
        print("File " + x +  ".txt has been removed")
    except FileNotFoundError:
        print("File " + x + ".txt not found")

    # Create new json file
    with open(COURSE_DATA_PATH + x + '.txt', 'w') as outfile:
        json.dump(data, outfile)
    print("File has been created")

driver.quit()