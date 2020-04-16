import json
from selenium import webdriver
import datetime


def lambda_handler(event, context):
    # get today and tomorrow dates
    today = datetime.datetime.today().strftime("%d %B %Y")
    tomorrow_raw = datetime.datetime.today() + datetime.timedelta(days=1)
    tomorrow = tomorrow_raw.strftime("%d %B %Y")

    # process input
    user_req = next(iter(event['queryStringParameters'])).split(" ")

    print(user_req)
    req_date = ""
    # get date from input
    if user_req[0] == "today":
        req_date = today
    elif user_req[0] == "tomorrow":
        req_date = tomorrow
    else:
        print("bad input")
        exit(2)

    # get meal from input
    meal_req = user_req[1].upper()

    # open selenium webdriver
    driver = webdriver.Chrome()
    driver.get("https://nutrition.grinnell.edu/NetNutrition/1#")

    # locate and click on grinnell marketplace button
    marketplace = driver.find_element_by_class_name("cbo_nn_sideUnitCell")
    marketplace.click()

    # get first three day objects
    first_three_days = driver.find_elements_by_class_name("cbo_nn_menuCell")[0:3]

    # get dates from first three objects
    first_three_dates = []
    for day in first_three_days:
        text = day.text
        date = text.split('\n')[0]
        first_three_dates.append(date)

    # get date object based on user req
    req_date_obj = first_three_days[first_three_dates.index(req_date)]

    # click on meal link based on user req
    meals = req_date_obj.find_elements_by_class_name("cbo_nn_menuLink")

    # click on requested meal
    meals_text = []
    for meal in meals:
        meals_text.append(meal.text)

    meals[meals_text.index(meal_req)].click()

    food_table = driver.find_elements_by_class_name("cbo_nn_itemGridTable")[0]

    food_table_row = food_table.find_elements_by_tag_name("tr")

    section_and_items = food_table_row[1:]

    menu = {}
    section = ""
    for i in section_and_items:
        if str(i.text).isupper():
            section = str(i.text)
            menu[section] = []
        else:
            menu[section].append(str(i.text).split("(")[0].rstrip())

    return ({
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(menu)
    })


# print(lambda_handler({"queryStringParameters": {"today lunch":""}}, ""))
