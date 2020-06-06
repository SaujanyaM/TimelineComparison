import pandas as pd
import json
import random
import datetime

activities_file = "categories.txt"
time_converter_file = "timeConverter.txt"
minutely_data_file = "minutely_data.txt"
demographics_data_file = "summary_total.txt"

def parse_activities():
    activities_csv = pd.read_csv(activities_file)
    activities = {}

    for row in activities_csv.itertuples():
        activities[row[1]] = row[2]

    activities = {'n1': 'Personal Care', 
                  'n1.1': 'Sleeping', 
                  'n2': 'Household activities', 
                  'n3': 'Family care', 
                  'n4': 'Family care',#'Nonfamily care', 
                  'n5': 'Work', 
                  'n5.1': 'Job search', 
                  'n6': 'Education', 
                  'n7': 'Shopping', 
                  'n8': 'Household activities', #Assorted services', 
                  'n9': 'Eating and drinking', 
                  'n10': 'Leisure', #Other leisure', 
                  'n10.1': 'Leisure', #,Socializing', 
                  'n10.2': 'Leisure', #'Relaxing and thinking', 
                  'n10.3': 'Leisure', #'TV and movies', 
                  'n10.4': 'Leisure', #'Computer use', 
                  'n11': 'Leisure', #'Sports', 
                  'n12': 'Leisure', #'Religious activities', 
                  'n13': 'Leisure', #'Volunteering', 
                  'n14': 'Leisure', #'Phone calls', 
                  'n15': 'Traveling', 
                  'n16': "Couldn't remember"}

    return activities

def parse_time():
    time_tsv = pd.read_csv(time_converter_file, delimiter="\t")
    time_converter = {}
    for row in time_tsv.itertuples():
        time_converter[row[1]] = row[2]

    return time_converter

def parse_minutely_data(activities, time_converter):
    minutely_tsv = pd.read_csv(minutely_data_file, delimiter="\t")
    minutely_data = {}

    selected_columns = [x+"-0" for x in activities.keys()]
    minutely_tsv = minutely_tsv[selected_columns]


    for row in minutely_tsv.itertuples():
        time_details = {}
        for i, elem in enumerate(row[1:]):
            activity_name = activities[selected_columns[i].replace("-0", "")]
            if activity_name in time_details:
                time_details[activity_name] += elem
            else:
                time_details[activity_name] = elem
        
        minutely_data[time_converter[row[0] + 1]] = time_details

    return minutely_data

def parse_demographics_data(activities):
    dem_tsv = pd.read_csv(demographics_data_file, delimiter="\t")
    dem_data = {}
    for index in dem_tsv.index:
        demographic = {}
        for k, v in activities.items():
            col = dem_tsv[k]
            demographic[v] = col[index]
        dem_data[dem_tsv["demTitle"][index]] = demographic
    return dem_data

def pick_random_activity(probabilities):
    random_target = random.random()
    cur_total = 0

    for key, value in probabilities.items():
        cur_total += value

        if cur_total >= random_target:
            return key

    return "Couldn't remember"


def generate_schedule(minutely_data, dem_data):
    schedule = {}
    people = []
    humans = [{"name": "Johnny", "dem": "Unemployed"}, {"name": "Tom", "dem": "Employed"}, {"name": "Bert", "dem": "Two+ Children"}]
    
    for human in humans:
        person = {"name": human["name"]}
        person_daily_schedule = []
        for day in range(5,5+10):
            current_time = datetime.datetime(2020, 3, day, 4)
            daily_schedule = {"day": current_time.strftime("%m/%d/%Y")}
            day_schedule = []
            #print("day---------------------------")
            for key, value in minutely_data.items():
                rand_activity = pick_random_activity(value)
                activity_object = {"starting_time": current_time.strftime("%H:%M"), 
                                   "end_time": (current_time+datetime.timedelta(minutes=10)).strftime("%H:%M"),
                                   "activity": rand_activity}

                day_schedule.append(activity_object)
                current_time += datetime.timedelta(minutes=10)

            daily_schedule["schedule"] = day_schedule
            person_daily_schedule.append(daily_schedule)

        person["daily_schedule"] = person_daily_schedule
        people.append(person)
    schedule["people"] = people
    return schedule

def add_activities_to_data(data, activities):
    activities_list = []
    for k, v in activities.items():
        if v not in activities_list:
            activities_list.append(v)
    data["activities"] = activities_list

def main():
    activities = parse_activities()
    print(activities)

    time_converter = parse_time()
    #print(time_converter)

    minutely_data = parse_minutely_data(activities, time_converter)
    #print(minutely_data.keys())

    dem_data = parse_demographics_data(activities)

    with open("output.json", "w") as f:
        f.write(json.dumps(minutely_data))

    schedule = generate_schedule(minutely_data, dem_data)
    add_activities_to_data(schedule, activities)

    with open("schedule.json", "w") as f:
        f.write(json.dumps(schedule))



if __name__ == "__main__":
    main()