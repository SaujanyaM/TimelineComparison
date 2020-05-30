import pandas as pd
activities_file = "categories.txt"
time_converter_file = "timeConverter.txt"
minutely_data_file = "minutely_data.txt"

def parse_activities():
    activities_csv = pd.read_csv(activities_file)
    print(activities_csv)
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

def parse_minutely_data():
    time_tsv = pd.read_csv(time_converter_file, delimiter="\t")
    time_converter = {}
    for row in time_tsv.itertuples():
        time_converter[row[1]] = row[2]

    return time_converter

def main():
    activities = parse_activities()
    print(activities)

    time_converter = parse_time()
    print(time_converter)


if __name__ == "__main__":
    main()