# dataframes
import pandas as pd
import re
import sys
from termcolor import colored, cprint
import requests
import time

safety_df = pd.read_csv("data/country_name_comparison - safety_index.csv")
cost_df = pd.read_csv("data/country_name_comparison - costofliving.csv")
gay_df = pd.read_csv("data/country_name_comparison - lgbtq_index.csv")
currency_df = pd.read_csv("data/country_name_comparison - country_currencies.csv")
democracy_df = pd.read_csv("data/country_name_comparison - democracy_index.csv")
language_df = pd.read_csv("data/country_name_comparison - country_languages.csv")
mountain_df = pd.read_csv("data/country_name_comparison - Mountain (1).csv")
coast_df = pd.read_csv("data/country_name_comparison - Coastline.csv")


# further data cleaning
def replace(string):
    string1 = re.sub(u"\xa0[a-z]+", "", string)
    string2 = re.sub("[,]", "", string1)
    string3 = re.sub(r"[\[\]]", "", string2)
    return string3

def replace2(string):
    if type(string)== str:
        string1 = re.sub(u"\xa0[a-z]+", "", string)
        string2 = re.sub("[,]", "", string1)
        string3 = re.sub(r"[\[\]]", "", string2)
        return string3

coast_df["Distance"] = coast_df["Distance"].apply(replace2)
coast_df["Distance"] = coast_df["Distance"].astype(float)

mountain_df["Maximum elevation"] = mountain_df["Maximum elevation"].apply(replace)
mountain_df["Maximum elevation"] = mountain_df["Maximum elevation"].astype(int)

# basic functions of programm

import pandas as pd

country_selection = []
visa_preference = ''
no_visa_needed = []
country = ""

def linebreak():
    """
    Print a line break
    """
    print("\n")

def start():
    """
    Start the programm and gives instructions
    """
    linebreak()
    print("Hello and welcome on the journey of finding your optimal travel location.")
    linebreak()
    print("You will have the opportunity to filter different categories and we will give you the best place for you to travel to. ")
    linebreak()
    text = colored("You can filter for your preferences regarding: currency, cost of living, language, lgbtq friendly, safety, democracy, mountains", "green", attrs=['reverse', 'blink'])
    print(text)
    next_action()

# function to decide wether or not choose a category

def next_action():
    """
    In this function you can decide wether you want to continue choosing categories or not.
    """
    answer = input("Do you want to choose a category? Answer with yes or no.")
    if answer == "yes":
        choose_category()
    elif answer == "no":    
        if country_selection == []:
            text = colored("To find your dream vacation, please choose a category", 'red', attrs=['reverse', 'blink'])
            print(text)
            choose_category()
        else:
            end_filter()
    else:
        text = colored("Sorry, we did not understand this.", 'red', attrs=['reverse', 'blink'])
        print(text)
        next_action()

# function to end program

def end_filter():
    """
    A function to end the filterinf and give the results.
    """
    q_result = input("If you want to see your dream destination type: result. If you want to continue filtering type: filter.")
    if q_result == "result":
        visa()
    elif q_result == "filter":
        choose_category()
    else:
        text = colored("Sorry, we couldn't understand you. Please type either result or filter.", 'red', attrs=['reverse', 'blink'])
        print(text)
        end_filter()

# filter for visa requirements

def visa():
    """
    This function asks for visa preferences and filters the countries with no visa requirements according to nationality.
    """
    global visa_preference
    global no_visa_needed
    #no_visa_needed = []
    print("We have a country selection for you. Would you be willing to apply for a visa for your vacation?")
    visa_preference = input("Please answer with yes or no.")
    if visa_preference == "yes":
        best_country()
    elif visa_preference == "no":
        print("Alright! First of all: what is your nationality?")
        nationality = input("Please enter the name of your country.")
        nationality = nationality.lower()
        if nationality == "spain":
            visa_spain = pd.read_csv("data/visa_spain.csv")
            selection = visa_spain.loc[visa_spain["Visa requirement"] == "no visa", ["Country"]]
            no_visa_needed.append(selection["Country"].to_list()) 
            best_country()
        elif nationality == "portugal":
            visa_portugal = pd.read_csv("data/visa_portugal.csv")
            selection = visa_portugal.loc[visa_portugal["Visa requirement"] == "no visa", ["Country"]]
            no_visa_needed.append(selection["Country"].to_list()) 
            best_country()
        elif nationality == "kenya":
            visa_kenya = pd.read_csv("data/visa_kenya.csv")
            selection = visa_kenya.loc[visa_kenya["Visa requirement"] == "no visa", ["Country"]]
            no_visa_needed.append(selection["Country"].to_list())
            best_country()
        elif nationality == "india":
            visa_india = pd.read_csv("data/visa_india.csv")
            selection = visa_india .loc[visa_india["Visa requirement"] == "no visa", ["Country"]]
            no_visa_needed.append(selection["Country"].to_list())
            best_country()
        elif nationality == "germany":
            visa_germany = pd.read_csv("data/visa_germany.csv")
            selection = visa_germany.loc[visa_germany["Visa requirement"] == "no visa", ["Country"]]
            no_visa_needed.append(selection["Country"].to_list())
            best_country()
        elif nationality == "argentina":    
            visa_argentina = pd.read_csv("data/visa_argentina.csv")
            selection = visa_argentina.loc[visa_argentina["Visa requirement"] == "no visa", ["Country"]]
            no_visa_needed.append(selection["Country"].to_list())
            best_country()
        else:
            text = colored("Sorry, we did not understand that.", 'red', attrs=['reverse', 'blink'])
            print(text)
            visa()     
    else:
        text = colored("Sorry, we did not understand that.", 'red', attrs=['reverse', 'blink'])
        print(text)
        visa()

# function to bring everything together and select final country

def best_country():
    """
    This function selects the winner from our chosen countries from before
    and returns all countries with the highest count in a list.
    """
    global visa_preference
    global no_visa_needed

    all_countries = [country for sublist in country_selection for country in sublist]
    if all_countries == []:
        text = colored("Sorry! We couldn't find a matching country. Please try again.", 'red', attrs=['reverse', 'blink'])
        print(text)
        start()
    else:
        from collections import Counter
        country_freq = dict(Counter(all_countries))
        final_dict = {}
        if visa_preference == "no":
            for country in country_freq:
                if country in no_visa_needed[0]:
                    final_dict[country] = country_freq[country]
                else:
                    continue
            max_value = max(final_dict.values())
        elif visa_preference == "yes":
            final_dict = country_freq
            max_value = max(country_freq.values())
        choice = [k for k,v in final_dict.items() if v == max_value]
        text = colored('Congratulations!!! We found the perfect place for your next holiday: ', 'green', attrs=['reverse', 'blink'])
        print(text)
        text = colored(choice, 'green', attrs=['reverse', 'blink'])
        print(text)
        country_info()

# choose your preferred country from the result and receive information

def country_info():
    """
    This function gives you a summary of information about the selected country.
    """
    global country
    print("From your personalised selection of countries, please choose on country to receive a summary of information.")
    country = input("Please write the name of your selected country.")
    country = country.capitalize()
    linebreak
    print("You selected: " + country)
    linebreak()
    weather()
    linebreak()
    curr_new = currency_df.set_index('CountryName').T
    curr = curr_new.index[curr_new[country]==1].to_list()
    print("Currency: ")
    print(curr)
    linebreak()
    lang_new = language_df.set_index("CountryName").T
    lang = lang_new.index[lang_new[country] == 1].to_list()
    print("Language: " + str(lang))
    linebreak()
    cost = cost_df.loc[cost_df["country"]== country, "costLiving_lc"]
    print("Cost of living: " + str(int(cost)))
    linebreak()
    safety = safety_df.loc[safety_df["Country"]== country, "Safety Index"]
    print("Safety level: " + str(int(safety)))
    linebreak()
    lgbtq = gay_df.loc[gay_df["CountryName"]== country, "Rank"]
    print("Rank of lgbtq friendliness: " + str(int(lgbtq)))
    linebreak()
    democracy = democracy_df.loc[democracy_df["Country"]== country, "Rank_2021"]
    print("Rank of democracy: " + str(int(democracy)))
    linebreak()
    mountain = mountain_df.loc[mountain_df["Country or region"]== country, "Maximum elevation"]
    print("Maximum elevation in m: " + str(round(int(mountain)/3.280)))
    linebreak()
    #coast = coast_df.loc[coast_df["Country"] == country, ["Distance"]]
    #print("The coastline is " + str(int(coast["Distance"]))+ " km long.")

    
    # function to choose category

def choose_category():
    """
    This funtion makes ou choose between different categories 
    that should be explored further.
    """
    
    action = input("Which category is important for you?").strip()
    if action == "currency":
        currency()
    elif action == "democracy":
        democracy()
    elif action == "cost of living":
        cost()
    elif action == "language":
        language()
    elif action == "lgbtq friendly":
        gay_friendly()
    elif action == "safety":
        safety()
    elif action == "mountains":
        mountain()
    #elif action == "coastline":
    #    coast()
    else:
        text = colored("""We are so sorry, this category doesn't exist. Please try another category:
        currency, cost of living, language, lgbtq friendly, safety, democracy, mountains""", 'red', attrs=['reverse', 'blink'])
        print(text)
        linebreak()
        choose_category()
        
# function for safety index

def safety():
    """
    This function asks for the minimun safety level required and adds all countries that fulfil the condition.
    These countries are then added to the selection of countries.
    """
    print("""What is your minimum safety level required? 
    You can choose between: low, medium, high, very high.""")
    level = input("Please write down the minimum safety level for your destination country.")
    if level == "low":
        country_selection.append(safety_df["Country"].to_list()) 
    elif level == "medium":
        selection = safety_df.loc[safety_df["Safety Index"] > 35, ["Country"]]
        country_selection.append(selection["Country"].to_list()) 
    elif level == "high":
        selection = safety_df.loc[safety_df["Safety Index"] > 55, ["Country"]]
        country_selection.append(selection["Country"].to_list()) 
    elif level == "very high":
        selection = safety_df.loc[safety_df["Safety Index"] > 75, ["Country"]]
        country_selection.append(selection["Country"].to_list()) 
    else:
        text = colored("This safety level doesn't exist.", 'red', attrs=['reverse', 'blink'])
        print(text)
        safety()
    text = colored("Thank you for choosing " + level + " in the safety category.", 'green', attrs=['reverse', 'blink'])
    print(text)
    linebreak()
    next_action()

    # function for cost of living

def cost():
    """
    This function asks for the maximum level of cost of living.
    The countries that fulfil the condition will be added to the selection of countries.
    """
    print("""What is the maximum level of cost of living your travel location should have. 
    You can choose between: low, medium, high, very high.""")
    level = input("Please choose your maximum level of cost of living.")
    if level == "low":
        selection = cost_df.loc[cost_df["costLiving_lc"] <= 600, ["country"]]
        country_selection.append(selection["country"].to_list()) 
    elif level == "medium":
        selection = cost_df.loc[cost_df["costLiving_lc"] <= 1200, ["country"]]
        country_selection.append(selection["country"].to_list())
    elif level == "high":
        selection = cost_df.loc[cost_df["costLiving_lc"] <= 1800, ["country"]]
        country_selection.append(selection["country"].to_list())
    elif level == "very high":
        country_selection.append(cost_df["country"].to_list())
    else:
        text = colored("This level of cost of living doesn't exist.", 'red', attrs=['reverse', 'blink'])
        print(text)  
        cost() 
    text = colored("Thank you for choosing " + level + " in the cost of living category.", 'green', attrs=['reverse', 'blink'])
    print(text)
    linebreak()
    next_action()

    # function for lgbtq friendliness of a country

def gay_friendly():

    """
    This function asks whether or not it is important for you that the vacation country 
    is not discriminative towards lqbtq and gives a list of fitting countries.
    """
    print("""How safe should your destination country at least be for lgbtq? 
    You can choose between dangerous, not safe, safe, very safe.""")
    level = input("Please enter the required minimum safety level!")
    if level == "dangerous":
        country_selection.append(gay_df["CountryName"].to_list()) 
    elif level == "not safe":
        selection = gay_df.loc[gay_df["Total"] >= -5, ["CountryName"]]
        country_selection.append(selection["CountryName"].to_list()) 
    elif level == "safe":
        selection = gay_df.loc[gay_df["Total"] >= 0, ["CountryName"]]
        country_selection.append(selection["CountryName"].to_list()) 
    elif level == "very safe":
        selection = gay_df.loc[gay_df["Total"] >= 5, ["CountryName"]]
        country_selection.append(selection["CountryName"].to_list()) 
    else:
        ttext = colored("This safety level doesn't exist.", 'red', attrs=['reverse', 'blink'])
        print(text)
        gay_friendly()
    text = colored("Thank you for choosing " + level + " in the lgbtq friendliness category.", 'green', attrs=['reverse', 'blink'])
    print(text)
    linebreak()
    next_action()
    
# function for the preferred currency
def currency():
   """
   This function asks for your preferred currency to pay with and gives a list of fitting countries.
   """
   print("""Please enter the currency of you in the official abreviation.""")
   value = input("Please enter the currency in the official abbreviation.")
   value = value.upper()
   if value in currency_df.columns:
      selection = currency_df.loc[currency_df[value] == 1, ["CountryName"]]
      country_selection.append(selection["CountryName"].to_list()) 
   else:
      text = colored("Sorry, we could not find this currency. Please try again and make sure to enter the official country abbreviation", 'red', attrs=['reverse', 'blink'])
      print(text)
      currency()
   text = colored("Thank you for choosing " + value + " as your preferred currency.", 'green', attrs=['reverse', 'blink'])
   print(text)
   linebreak()
   next_action()
   
# function for democracy index of country
def democracy():
    """
    This function asks for the minimum democracy level required and gives a list of fitting countries.
    """
    print("""What is your minimum democracy level required for your destination country?
    You can choose between low, medium, high and very high.""")
    level = input("Please enter your minimum democracy level required.")
    if level == "low":
        country_selection.append(democracy_df["Country"].to_list()) 
    elif level == "medium":
        selection = democracy_df.loc[democracy_df["Index_2021"] > 4, ["Country"]]
        country_selection.append(selection["Country"].to_list())
    elif level == "high":
        selection = democracy_df.loc[democracy_df["Index_2021"] > 7, ["Country"]]
        country_selection.append(selection["Country"].to_list())
    elif level == "very high":
        selection = democracy_df.loc[democracy_df["Index_2021"] > 8.5, ["Country"]]
        country_selection.append(selection["Country"].to_list())
    else:
        text = colored("This democracy level doesn't exist.", 'red', attrs=['reverse', 'blink'])
        print(text)    
        democracy() 
    text = colored("Thank you for choosing " + level + " in the democracy category.", 'green', attrs=['reverse', 'blink'])
    print(text)
    linebreak()
    next_action()

# function for language

def language():
    """
    This function asks which language do you prefer to speak and gives a list of fitting countries.
    """
    print("""Which language do you prefer to speak? 
    You can choose this category multiple times if you want to choose multiple languages.""")
    lang = input("Please enter the language of your preference.")
    lang = lang.capitalize()
    if lang in language_df.columns:
        selection = language_df.loc[language_df[lang] == 1, ["CountryName"]]
        country_selection.append(selection["CountryName"].to_list())
    else:
        text = colored("Sorry, we could not find this language.", 'red', attrs=['reverse', 'blink'])
        print(text) 
        language()
    text = colored("Thank you for choosing " + lang + " as your preferred language.", 'green', attrs=['reverse', 'blink'])
    print(text)
    linebreak()
    next_action()
        
#function for countries that have mountains

def mountain():
    """
    This function filters for countries that have mountains.
    """
    print("Is it important for you that a country has mountains?")
    answer = input("Please type yes or no.")
    if answer == "yes":
        selection = mountain_df.loc[mountain_df["Maximum elevation"] > 3280, ["Country or region"]]
        country_selection.append(selection["Country or region"].to_list())
    elif answer == "no":
        country_selection.append(mountain_df["Country or region"].to_list())
    else:
        text = colored("Sorry, we didn't understand you.", 'red', attrs=['reverse', 'blink'])
        print(text) 
        mountain()
    text = colored("Thank you for giving your preferrence regarding mountains.", 'green', attrs=['reverse', 'blink'])
    print(text)
    linebreak()
    next_action()

#function for countries that have coast line

# def coast():
#     """
#     This function filters for countries that have a coastline.
#     """
#     print("Is it important for you that a country has a coastline?")
#     answer = input("Please type yes or no.")
#     if answer == "yes":
#         selection = coast_df.loc[coast_df["Distance"] > 0, ["Country"]]
#         country_selection.append(selection["Country"].to_list())
#     elif answer == "no":
#         country_selection.append(coast_df["Country"].to_list())
#     else:
#         text = colored("Sorry, we didn't understand you.", 'red', attrs=['reverse', 'blink'])
#         print(text) 
#         coast()
#     text = colored("Thank you for giving your preferrence regarding coastline.", 'green', attrs=['reverse', 'blink'])
#     print(text)
#     linebreak()
#     next_action()

# function that gives the current weather & temperature in selected country

def weather():
    """
    This function gives the current weather & temperature for the selected country. 
    """
    global country
    url = "https://community-open-weather-map.p.rapidapi.com/weather"
    querystring = {"q":country,"lang":"eng","units":"metric"}
    headers = {
	    "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
	    "X-RapidAPI-Key": "5f923a0d42msh3a49a095d38db66p176833jsne813ae937562"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    time.sleep(3)
    weather_data=(response.json())
    name  = weather_data["name"]
    weather = weather_data['weather'][0]['main']
    temp = weather_data['main']['temp']
    data = []
    data.append({'Country' : name, 'Weather' : weather, 'Temperature' : temp})
    pd.DataFrame(data)
    Forecast=pd.DataFrame(data)
    print("The current temperature is " + str(float(Forecast["Temperature"])) + "° and the weather is " + str(Forecast.iat[0,1])+ ".")



start()