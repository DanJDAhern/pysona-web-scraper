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
    
def get_section(id):

    class_string = "SectionContainer"+str(id)

    date = ""
    day  = ""
    
    section = soup.find("div", id=class_string)
    all_rows = section.find_all("tr")
    del all_rows[0:3]
    line = []

    for row in all_rows:
        row_data = row.find_all("td")
        for entry in row_data:
            parse_special_items(entry) 

            data_entry = {'Date': date, 'Day': day, 'Time of Day': "Day", 'Action Type': "Action", 'Missable': "", 'Steps': []}
            steps = []
            entry_text = entry.text



            if entry_text[0].isdigit():
                date = entry_text[0:5] 
                day = entry_text[5:8] 

                data_entry['Date'] = date 
                data_entry['Day'] = day
            else:
                if (len(diary) != 0):
                   
                    if (day == diary[len(diary)-1]['Day']) :
                        data_entry['Time of Day'] = "Night"

                steps.append(entry_text.split(";"))
                data_entry['Steps'] = steps

                data_entry['Action Type'] = get_action_type(entry_text.upper())
        
            if len(steps) > 0:
                diary.append(data_entry)

def get_action_type(input):
    output = None

    # Book items
    if "READ THE BOOK" in input:
        return "Read Book"

    elif ("GO TO" in input or "GO" in input):
        return "Travel"



    
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


while(proceed):
   
    scrape_dates()
    egg = process_section(2, "april")
    get_section(2)
    proceed = False
# Convert to pandas DataFrame for easier manipulation
df = pd.DataFrame(diary)
df.to_csv("Export.csv")
# Display the DataFrame
print(df)