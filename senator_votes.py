import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import time
from all_senators import senator_list
votes = []
for i in range(1, 166, 1):
    if len(str(i)) == 1:
        vote = "0000" + str(i)
    elif len(str(i)) == 2:
        vote = "000" + str(i)
    else:
        vote = "00" + str(i)
    votes.append(vote)

#votes = votes[:5]

results = []
senator_name = input('Type in name of senator to search. Last name only. ')
get_senator_name = 0
for senator in senator_list:
    if senator_name in senator:
        get_senator_name = senator
if get_senator_name:
    print(get_senator_name)
else:
    print("Senator not in list")


categories = ['Question:','Vote Number:', 'Vote Date:', 'Required For Majority:', 'Vote Result:',
          'Nomination Number:', 'Nomination Description:', '']
get_url = "https://www.senate.gov/legislative/LIS/roll_call_lists/roll_call_vote_cfm.cfm?congress=115&session=1&vote="
for vote in votes:
    time.sleep(1)
    full_url = get_url + vote
    page = requests.get(full_url)
    print(page.status_code)
    if page.status_code != 200:
        continue
    soup = BeautifulSoup(page.content, 'lxml')
    content_text = soup.find(class_ = "contenttext")
    voting = soup.find(class_ = "newspaperDisplay_3column")


    for i in range(0, len(categories), 1):
        if i + 1 < len(categories):
            if categories[i] == 'Vote Result:' and 'Nomination' not in content_text.text:
                search_string = categories[i] + '.*'
            else:
                search_string = categories[i] + '.*' + categories[i+1]
            question = re.findall(search_string, content_text.text, re.DOTALL)
            question = ''.join(question)
            question = question.replace(categories[i], '').replace(categories[i+1], '').strip(' ').strip('\n')
            results.append(question)

    get_senator_name_v2 = get_senator_name.replace('(', '\(').replace(')', '\)')
    if senator_list.index(get_senator_name) == len(senator_list) - 1:
        get_next_senator = ''
        get_next_senator_v2 = ''
    else:
        get_next_senator = senator_list.index(get_senator_name) + 1
        get_next_senator = senator_list[get_next_senator]
        get_next_senator_v2 = get_next_senator.replace('(', '\(').replace(')', '\)')

    search_string = get_senator_name_v2 + '.*' + get_next_senator_v2
    question = re.findall(search_string, voting.text, re.DOTALL)
    question = ''.join(question)
    question = question.replace(get_senator_name, '').replace(get_next_senator, '').strip(' ').strip('\n').strip(', ')
    results.append(question)





question_list = []
vote_number = []
vote_date = []
required_for_majority = []
vote_result = []
nomination_number = []
nomination_description = []
cardin_vote = []
get_index = -1
for result in results:
    get_index = get_index + 1
    if get_index % 8 == 0:
        get_index = 0
    if get_index == 0:
        question_list.append(result)
    elif get_index == 1:
        vote_number.append(result)
    elif get_index == 2:
        vote_date.append(result)
    elif get_index == 3:
        required_for_majority.append(result)
    elif get_index == 4:
        vote_result.append(result)
    elif get_index == 5:
        nomination_number.append(result)
    elif get_index == 6:
        nomination_description.append(result)
    else:
        cardin_vote.append(result)

get_votes = pd.DataFrame({
    "Question": question_list,
    "Vote Number": vote_number,
    "Vote Date": vote_date,
    "Required for Majority": required_for_majority,
    "Vote Result": vote_result,
    "Nomination Number": nomination_number,
    "Nomination Description": nomination_description,
    "Vote": cardin_vote,

})


get_senator_name = get_senator_name.replace(' ', '_').replace('(', '').replace(')', '')
csv_file = get_senator_name + '.csv'
get_votes.to_csv(csv_file)
