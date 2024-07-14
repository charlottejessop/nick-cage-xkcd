import requests
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import numpy as np
import math


def call_url(url, count):
    if count % 20 == 0:
        print("Completing Request Num:", count)
    try:
        r = requests.get(url)
        return r.json()
    except:
        pass

def multiple_xkcd(min_val, max_val):
    x = min_val 
    url_list = []
    while x <= int(max_val):
        #insert number into https://xkcd.com/{x}/
        new_address = f'https://xkcd.com/{x}/info.0.json'
        url_list.append(new_address)
        x = x + 1 #ends with list of non-called addresses
    return url_list
   


def get_dates(request_results): #shows dates published for given range of comics
    dates_dict = dict()
    list2 = [] 
    for x in request_results:
        if x is None:
            continue
        date = int(x['day']), int(x['month']), int(x['year']) 
        list2.append(date)
    for c in list2:
        dates_dict[c] = dates_dict.get(c, 0) + 1
    return dates_dict
    
def how_many_word(request_results): #prompts for word, says how many of that word appears in given range
    word1 = input("Please enter a word: ")
    word_count = 0
    l = []
    for y in request_results:                   
        if y == None:
            continue
        x = y['transcript']
        # splits it by lines
        line_lists = x.split("\n")
        for word in line_lists:
            if word.startswith("[") or word.startswith("{"):
                # skip
                continue
            else:
                wordsInLine = word.split()
                # go through each word in the line and remove non-letters
                filteredWords = []
                for word in wordsInLine:
                    #strip any characters
                    filtered = ''.join(filter(str.isalpha, word))##
                    filteredWords.append(filtered)
                # split the words by spaces
                l += filteredWords
        new_l = []
        for words in l:
            new_l.append(words.lower())
        for word in new_l:
            if word == word1:
                word_count += 1 
    print(word_count, "occurences across all specificed XKCDs")

def collate_words(max_val, min_val): #collates list of all words in range
    url_list = multiple_xkcd(min_val, max_val)
    l = []
    request_results = []
    count = 0
    for i in url_list:  
        y = call_url(i, count)
        request_results.append(y)
        count += 1
        if y == None:
            continue
        x = y['transcript']
        # splits it by lines
        line_lists = x.split("\n")
        for word in line_lists:
            if word.startswith("[") or word.startswith("{") or word.startswith(" ") or word == '': 
                continue
            else:
                wordsInLine = word.split()
                # go through each word in the line and remove non-letters
                filteredWords = []
                for word in wordsInLine:
                    #strip any characters
                    filtered = ''.join(filter(str.isalpha, word))##  
                    if filtered != '':
                        filteredWords.append(filtered)
                # split the words by spaces
                l += filteredWords
    return (l, request_results)

def words(min_val, max_val): 
    l, request_results = collate_words(max_val, min_val) #list of all words in range
    new_l = dict()
    for words in l:
        if words not in new_l:
            new_l[words.lower()] = 1
        else:
            new_l[words.lower()] += 1 #returns dict of word count for every word in range
    return new_l, request_results
 
def most_popular_word(min_val, max_val): #recommended range of at least 500 #returns most popular word
    new_l, request_results = words(min_val, max_val)
    maximum1 = max(new_l, key = new_l.get)
    # checks for other keys that have the same count as the minimum
    res = [key for key in new_l if new_l[key] == new_l[maximum1]]

    if len(res) > 1:
        print("The most popular words were: " + str(res))
    # there will always be one word: the minimum
    else:
        print("The most popular word is: " + str(maximum1)) 

    return maximum1, request_results



def pop_word_trend(request_results, popular_word): #min recommended range is 1095 #finds most popular word in range
        
    dates_dict = get_dates(request_results) #returns dictionary of all dates 
    for key in dates_dict.keys():
        dates_dict[key] = 0 #wipes all dictionary values back to 0, so only have dates
    l = []
    list3 = [] 
    for y in request_results: 
        
        if y == None:
            continue
        x = y['transcript']
        # splits it by lines
        line_lists = x.split("\n")
        for word in line_lists:
            if word.startswith("[") or word.startswith("{") or word.startswith(" ") or word == '':
                # skip
                continue
            else:
                wordsInLine = word.split()
                # go through each word in the line and remove non-letters
                filteredWords = []
                for word in wordsInLine:
                    #strip any characters
                    filtered = ''.join(filter(str.isalpha, word))##
                    if word != '':
                        filteredWords.append(filtered)
                    if word == popular_word: 
                        date = int(y['year']) 
                        list3.append(date)     
                # split the words by spaces
                l += filteredWords

    result = dict()
    for c in list3:
        result[c] = result.get(c, 0) + 1
    return result




def nick_cor(dates_dict): #generates graph of how often most popular word was used over specified range, compares to 
    #how many movies nick cage did over those years. then prints out r2
    # [(2006, 10)]
    els = list(dates_dict.items()) 
    x = int(els[0][0])
    t = int(els[-1][0])
    f = []
    for m in els:
        f.append(m[1])
    nick_dict = {2006: 4, 2007: 5, 2008: 2, 2009: 4, 2010: 4, 2011:5, 2012: 2, 2013: 2,
        2014: 5, 2015: 3, 2016: 5, 2017: 4, 2018: 8, 2019: 6, 2020: 4, 2021: 4, 2022: 1, 2023: 6, 2024: 4}
    nick_list = list(nick_dict.items())
    newer_list = []
    y = []
    for i in nick_list:
        newer_list.append(i[0])
    for z in newer_list:
        if t <= z >= x:
            y.append(z)
        else:
            continue

    nick_cage_movies = [nick_dict[year] * 20 for year in dates_dict.keys()]
    # times by 20 for better viewing in graph
    date_dict_words = list(dates_dict.values())

    nick_year_values = list(dates_dict.keys())

    X_axis = np.arange(len(nick_year_values))

    plt.bar(X_axis - 0.2, date_dict_words, 0.4, label = 'Max. Word Occurrences')
    plt.bar(X_axis + 0.2, nick_cage_movies, 0.4, label = 'Nick Cage Movies')

    plt.xticks(X_axis, nick_year_values)
    plt.yticks(visible=False)
    plt.xlabel("Years")
    plt.ylabel("Frequency")
    plt.title("Popular Word Use in XKCD vs. Nick Cage Movies")
    plt.legend()
    plt.show()


    # r2 is not well defined for less than 2 samples
    if len(date_dict_words) < 2:
        return

    r2 = round(r2_score(date_dict_words, nick_cage_movies), 2) 
    print(r2)

    if math.isnan(r2):
        return

    print('r2 score for perfect model is', r2) #prints r2, comments on strength of relationship
    if -0.3 <= r2 <= 0.3:
        print("There is a weak correlation. You are safe, for now.")
    elif 0.3 < r2 <= 0.7 or -0.3 > r2 >= -0.7:
        print("There is a moderate correlation. Beware.")
    else:
        print("There is a strong correlation. Don't trust anybody.")
    if len(nick_dict) < 5:
        print("Note: Data set limited, results may be inaccurate")

def get_range():
    while True:
        min_val = input("Enter ID start of query range (i.e. 5): ")
        if min_val.isdigit():
            break
        else:
            print("Please use a number")

    while True:
        max_val = input("Enter ID end of query range (i.e. 200): ")
        if max_val.isdigit():
            break
        else:
            print("Please use a number")

    return (int(min_val), int(max_val))

def confirm(text):
    while True:
        answer = input(f"{text} (Y/N): ")
        if answer in ["Y", "y", "N", "n"]:
            return answer.lower()
        else:
            print("Please reply with either Y or N")

def want_word_check(request_results):
    user_reply = confirm("Do you want to search for the amount of time a word has come up?")
    if user_reply == "n": return
    how_many_word(request_results)

def want_dates_check(request_results):
    user_reply = confirm("Can I interest you in some useless knowledge?")
    if user_reply == "n": return
    knowledge = get_dates(request_results)
    print(knowledge)
    print("These are the frequency of dates these comics were printed on")

MIN_VAL, MAX_VAL = get_range()

word, request_results = most_popular_word(MIN_VAL,MAX_VAL)
want_word_check(request_results)
dates_dict = pop_word_trend(request_results, word)
nick_cor(dates_dict)
want_dates_check(request_results)

print("Complete")