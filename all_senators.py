import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import time

get_url = "https://www.senate.gov/legislative/LIS/roll_call_lists/roll_call_vote_cfm.cfm?congress=115&session=1&vote=00001"
page = requests.get(get_url)
soup = BeautifulSoup(page.content, 'lxml')
voting = soup.find(class_ = "newspaperDisplay_3column")
#print(voting.text)
senators_list = voting.text.split('\n')
#print(senators_list)
senator_list_2 = []
for senator in senators_list:
    senator = senator.replace(', Yea', '')
    senator = senator.replace(', Nay', '')
    senator = senator.replace(', Not Voting', '')
    senator_list_2.append(senator)
    if senator == '':
        senator_list_2.remove(senator)

#print(senator_list_2)

senators_string = ''.join(senator_list_2)
#senators = re.findall(r"[\w']+", senators_string)
#print(senators)
senators = senators_string.split(")")
#print(senators)
senator_list = []
for senator in senators:
    senator = senator + ')'
    senator_list.append(senator)


if ')' in senator_list:
    senator_list.remove(')')
print(senator_list)
print(len(senator_list))


senator_names = []
party = []
state = []

party_options = ['D', 'R']
state_options = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL',
                 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME',
                 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH',
                 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI',
                 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI',
                 'WY']
