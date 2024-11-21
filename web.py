import requests
from bs4 import BeautifulSoup
import pandas as pd

current_page = 1
proceed = True

# To store the results in a list
data = []
diary = []
url = "https://psnprofiles.com/guide/11946-persona-5-royal-100-perfect-schedule"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

def process_section(input_id, date_id):

    # Create the URL for the section
    section = str(input_id)+"-"+str(date_id)
    found_section = soup.find_all("div", id=section)
    return found_section

# Takes in a row of HTML and parses the contents to determine applied styling.
# Based on the styling used on the original guide, we're able to differentiate item types.

def parse_special_items(line):

    text_to_parse = line.find("span", attrs={'style':'color:rgb(65,168,95)'})
    item = {"Item Name": "", "Item Type" : ""}
    item_array = []
    
    #if "READ THE BOOK" in temp_text:
       # data_entry['Action Type'] = "Book"

    #elif ("GO TO" in temp_text or "GO" in temp_text):
        #data_entry['Action Type'] = "Travel"

# Creates and returns the correct complete CSS class using inputted ID.
def get_class_string(id):
    return "SectionContainer"+str(id)

# Uses created class string to isolate section container from the website.
# Returns all rows held within that section for further processing.
def get_section_container(class_string):

    section = soup.find("div", id=class_string)
    all_rows = section.find_all("tr")
    del all_rows[0:3] # Trims out the starting preamble from the list so we purely have tasks.
    return all_rows

# Takes in the section container and breaks down each row into table data cells from which to extract data.
def extract_cells(section_container):
    for cell in section_container:
        segment = cell.find_all("td")
        date = format_date(segment[0].text)
        day = format_day(segment[0].text)
        day_tasks = segment[1].text.split(";")
        night_tasks = None

        
        store_task_in_diary(build_task_package(date, day, "Day", day_tasks))

        if len(segment) > 2:
            night_tasks = segment[2].text.split(";")
            store_task_in_diary(build_task_package(date, day, "Night", night_tasks))
            
        
    return 

def build_task_package(date, day, time_of_day, tasks):
    task = {}
    task['date'] = date
    task['day'] = day
    task['time_of_day'] = time_of_day
    task['tasks'] = tasks

    return task

def store_task_in_diary(task):
    diary.append(task)

def get_action_type(input):

    # Identifies actions which involve reading a book.
    if "READ THE BOOK" in input:
        return "Read Book"
    
    # Identifies actions which involve travelling from one location to another.
    elif ("GO TO" in input or "GO" in input):
        return "Travel"

def format_date(date):
    return date[0:5]

def format_day(day):
    return day[5:8]
    
def test(row_data):
    for row in row_data:
        creeate_task_package(row)

def creeate_task_package():
    date = None
    day  = None

    data_entry = {'Date': date, 'Day': day, 'Time of Day': "Day", 'Action Type': "Action", 'Missable': "", 'Steps': []}
    steps = []
    entry_text = input.text

    for row in input:
        row_data = input.find_all("td", attrs={'style':'text-align:justify'})
        for entry in row_data:
            if entry_text[0].isdigit():
                date = format_date(entry_text) 
                day = format_day(entry_text)

                data_entry['Date'] = date 
                data_entry['Day'] = day
            
                if (len(diary) != 0):
                    if (day == diary[len(diary)-1]['Day']) :
                        data_entry['Time of Day'] = "Night"
                steps.append(entry_text.split(";"))
                data_entry['Steps'] = steps
                data_entry['Action Type'] = get_action_type(entry_text.upper())
            
                diary.append(data_entry)
        


    
def scrape_dates():
    # Get and parse the page

    # Find all <td> elements with the desired style
    all_days = soup.find_all("td", style="width:2.9732%;text-align:center;") # Pulls dates/days
    all_rows = soup.find_all("tr")
    all_steps = soup.find_all("td", style="text-align:justify;") # Pulls steps per day

    #for row in all_rows:
      #  data = row.find("td", style="width:2.9732%;text-align:center;")
       # day = data.text
       # date = data.text

    # Extract data for each <td>
    for day in all_days:
        item = {}
        # Extract the content of the <td> element
        content = day.text
        # If there are at least two lines (Date and Day)
        item['Date'] = content[0:5] # Date (e.g., 04/09)
        item['Day'] = content[5:8]  # Day (e.g., Sat)
        data.append(item)  # Add the extracted data to the list

    # Print the number of days found
   # print(f"Total days found: {len(all_days)} Table: {all_rows[0]}")
    proceed = False

def main():
    # Construct Class String
    class_string = get_class_string(2)
    # Isolate section container for the selected month
    section_container = get_section_container(class_string)
    # Process Rows
    extract_cells(section_container)



    # Convert to pandas DataFrame for easier manipulation
    df = pd.DataFrame(diary)
    df.to_json("Export.json")
    # Display the DataFrame
    print(df)
    proceed = False

while(proceed):
   
    main()
    proceed = False
