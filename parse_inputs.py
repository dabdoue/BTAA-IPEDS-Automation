from datetime import date
import os.path

def parse_inputs(args_list):
    inputs = [[], ""]
    unitIDs = ""

    if len(args_list) > 1:
        for i in range(1, len(args_list)):
            file = args_list[i]
            if str(file) == "years_list.txt":
                years_file = open(file, "r")
                years = years_file.readlines()
                years_file.close()
                todays_date = date.today()
                for idx, year in enumerate(years):
                    if int(year) > int(todays_date.year) or int(year) < 1980:
                        print("At leat one invalid year given, please enter years no less than 1980")
                        quit()
                    years[idx] = year.rstrip()
                inputs[0] = years
            else:
                if os.path.isfile(file):
                    uid_file = open(file, "r")
                    uids = uid_file.readlines()
                    uid_file.close()
                    for uid in uids:
                        unitIDs += (uid[:uid.index('|')]) + ", "
                    if len(unitIDs) % 8 != 0:
                        print("Valid file with UnitIDs not given, please try again with a valid file.")
                        quit()
                    inputs[1] = unitIDs
                else:
                    print("File entered does not exist, please try again with a valid path to the file.")
                    quit()
    if inputs[0] != []:
        print("Years: " + ", ".join(inputs[0]))
    if inputs[1] != "":
        print("UnitIDs: " + inputs[1])
    return inputs