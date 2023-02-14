import shutil
import os
from pathlib import Path
import csv
import numpy as np
import pandas as pd
import time as time

def get_all_data(num_files):
    all_data = []
    file_offset = 0
    downloads_path = Path.home() / "Downloads"
    files = sorted(downloads_path.iterdir(), key=os.path.getmtime)
    # collect data from each csv file (each file is data for a single year)
    for j in range(0, num_files):
        # below code makes sure that the file to unzip is one that was downloaded from IPEDs
        # and also a file that has not been unzipped previously
        file_count = file_offset + 1
        file_name = ""
        file_dir = ""

        while ".zip" not in file_name and "CSV" not in file_name:
            file_dir = str(files[len(files) - (file_count)])
            file_name = file_dir[file_dir.rfind("\\") + 1:]
            file_count += 1

        file_offset = file_count - 1
        
        # below code gets the name of the csv that was extracted from zip
        # also makes sure file naming is correct
        cwd = os.getcwd()
        shutil.unpack_archive(file_dir, cwd)
        if " " in file_name:
            file_name = file_name[:file_name.index(" ")] + file_name[file_name.index("."):]
        file_no_ext = file_name.replace(".zip", "")
        csv_name = file_no_ext + ".csv"
        
        # opens csv file and puts text into data variable
        with open(csv_name, newline='') as f:
            reader = csv.reader(f)
            data = list(reader)

        # defining variables to be used as indexes for data to be referenced later
        private_expenses_idx = -1
        region_idx = -1
        land_grant_idx = -1
        research_expenses_idx = -1

        # changes each column header from original csv to have correct name
        for idx, column in enumerate(data[0]):
            if "institution name" in column:
                data[0][idx] = "Institution Name"
            if "year" in column:
                data[0][idx] = "Year"
            if "BEA" in column:
                data[0][idx] = "Geographic Region per IPEDs"
                region_idx = idx
            if "Land Grant Institution" in column:
                data[0][idx] = "Land Grant Institution"
                land_grant_idx = idx
            if "Total  enrollment" in column:
                data[0][idx] = "Total Students (Full-Time & Part-Time)"
            if "Full-time enrollment" in column:
                data[0][idx] = "Full-Time Students"
            if "Full-time undergraduate enrollment" in column:
                data[0][idx] = "Full-Time Undergraduates"
            if "Full-time graduate enrollment" in column:
                data[0][idx] = "Full-Time Graduates"
            if "Doctor's degree - research/scholarship" in column:
                data[0][idx] = "Research PhDs Awarded"
            if "Instructional, research and public service FTE" in column or "FTE staff" in column:
                data[0][idx] = "Full-Time Faculty (Instruction, Research, and Public Service)"
            if "Instructional FTE" in column:
                data[0][idx] = "Full-Time Faculty (Instruction Only)"    
            if "Research-Total amount" in column:
                data[0][idx] = "Research Expenditures (Private School)"
                private_expenses_idx = idx
            if "Research - Current year total" in column:
                data[0][idx] = "Research Expenditures"
                research_expenses_idx = idx
        # modifies values for data to be what we are looking for
        for i in range(1, len(data)):

            private_expenses = data[i][private_expenses_idx]
            region = data[i][region_idx]
            land_grant = data[i][land_grant_idx]

            # checks to see if private expense was left blank
            # if so, then school is public, otherwise private
            # also moves value of private school research expenses column to column for public school, then later deletes private school column 
            if private_expenses == '':
                data[i].append("Public")
            else:
                data[i].append("Private")
                data[i][research_expenses_idx] = private_expenses
            
            # only shows important value for region of school
            data[i][region_idx] = region[:region.index("(")].rstrip()

            # changes land grant values to just be yes or no
            if "Not" in land_grant:
                data[i][land_grant_idx] = "No"
            else:
                data[i][land_grant_idx] = "Yes"
        
        # adds another column to csv for public/private university data
        data[0].append("Public/Private University")
        
        # converts data so that entire column/row can be deleted
        n = len(max(data, key=len))
        data = [x + [None]*(n-len(x)) for x in data]
        data = np.array(data)
        # deletes private expenses column
        data = np.delete(data, private_expenses_idx, axis=1)
        # deletes UnitID column
        data = np.delete(data, 0, axis=1)

        # sets up and adds to variable that stores data from all collected years
        if j != 0:
            # deletes the first row if adding to data from other years, only need column headers 1 time 
            data = np.delete(data, 0, 0)
            # adds data for currently parsed year to all data
            all_data = np.vstack((all_data, data))
        else:
            # instantiates variable to store all data
            all_data = data
        
        # deletes html and csv file that were extracted from zip file, no longer needed
        os.remove(file_no_ext + ".csv")
        os.remove(file_no_ext + ".html")

    # stores all data as a csv   
    filename = "file" + str(time.time()) + ".csv"
    pd.DataFrame(all_data).to_csv(filename,index=False,header=False)
    return filename

