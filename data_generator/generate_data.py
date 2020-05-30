import pandas as pd
import json
import random

activities_file = "categories.txt"
time_converter_file = "timeConverter.txt"
minutely_data_file = "minutely_data.txt"

def parse_activities():
    activities_csv = pd.read_csv(activities_file)
    activities = {}

    for row in activities_csv.itertuples():
        activities[row[1]] = row[2]

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
            time_details[activity_name] = elem
        
        minutely_data[time_converter[row[0] + 1]] = time_details

    return minutely_data

def pick_random_activity(probabilities):
    random_target = random.random()
    cur_total = 0

    for key, value in probabilities.items():
        cur_total += value

        if cur_total >= random_target:
            return key

    return "this_failed"


def generate_schedule(minutely_data):
    schedule = {}

    for key, value in minutely_data.items():
        rand_activity = pick_random_activity(value)

        schedule[key] = rand_activity

    return schedule


def main():
    activities = parse_activities()
    #print(activities)

    time_converter = parse_time()
    #print(time_converter)

    minutely_data = parse_minutely_data(activities, time_converter)

    with open("output.json", "w") as f:
        f.write(json.dumps(minutely_data))

    schedule = generate_schedule(minutely_data)

    with open("schedule.json", "w") as f:
        f.write(json.dumps(schedule))



if __name__ == "__main__":
    main()