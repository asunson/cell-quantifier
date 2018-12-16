# import necessary packages 
import glob
import os
import pandas as pd
import quantify

# path = "/Users/ASun/Documents/2018-19/iPython Notebooks/Exp. 21/LEC co-culture/"

# read experiments to quantify from user modified text file

file = open("paths.txt", "r") 
experiments = file.readlines()

# find all culture types used within each experiment
for e in experiments:
    culture_types = [e + d + "/" for d in os.listdir(e) if os.path.isdir(os.path.join(e, d))]
    
    # iterate through experimental conditions within each culture type
    for path in culture_types:
        experiment_conditions = [path + d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

        # create excel sheet to store quantification results for a given culture and corresponding conditions
        writer = pd.ExcelWriter(path + "Quantification Results.xlsx")
        
        # each condition contains images to be quantified. Scan through each and run quantifying script
        for experiment in experiment_conditions:
            # create a subdirectory to store annotated cell count images if one does not already exist
            directory = experiment + "/Cell Counts"
            if not os.path.exists(directory):
                os.makedirs(directory)

            # collect list of all tif files within each folder
            imgnames = [i for i in glob.glob(experiment + "/*.tif")]
            imgnames.sort()

            print("******")
            print("Now quantifying: ", experiment.split('/')[-1])
            print("******")

            # quantify cell counts and thresholds 
            raw_imgnames, final_cell_counts, thresholds = quantify.quantifyCells(imgnames)
            
            # output final cell counts and thresholds corresponding to each image into excel sheet
            d = {"File Name": raw_imgnames, "Cell Count": final_cell_counts, "Threshold": thresholds}
            df = pd.DataFrame(data = d)
            df.to_excel(writer, experiment.split('/')[-1])
    
        writer.save()
        print("Done with Culture: ", path.split('/')[-2])
    print("Done with Experiment: ", e.split('/')[-2])
