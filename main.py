# import necessary packages 
import glob
import os
import pandas as pd
import quantify

def parseText(text):
    res = [l.strip('\n') for l in text if not l.startswith('#')]
    res = [l for l in res if l is not '']
    return res

# read experiments to quantify from user modified text files
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

file = open(os.path.join(__location__, 'paths.txt'), "r") 
experiments = file.readlines()

file = open(os.path.join(__location__, 'ignore.txt'), "r") 
ignore = file.readlines()

# remove comments from input text files
experiments = parseText(experiments)
ignore = parseText(ignore)

print(experiments)
print(ignore)


# find all culture types used within each experiment
for e in experiments:
    e_name = e.split(os.sep)[-1]

    # ask for user input before proceeding with experiment number
    print("********** Now looking at " + e_name + "**********")
    
    response = ''
    while(True):
        response = input('Would you like to proceed? (y/n)')
        if response in ['y', 'n']:
            break
    if response == 'n':
        continue

    culture_types = [os.path.join(e, d) 
                        for d in os.listdir(e) 
                        if os.path.isdir(os.path.join(e, d))]
    
    # iterate through experimental conditions within each culture type
    for culture in culture_types:
        culture_name = culture.split(os.sep)[-1]

        experiment_conditions = [os.path.join(culture, d) 
                                    for d in os.listdir(culture) 
                                    if os.path.isdir(os.path.join(culture, d))]

        # create excel sheet to store quantification results for a given culture and corresponding conditions
        writer = pd.ExcelWriter(os.path.join(culture, 
            culture_name + " Quantification Results.xlsx"))
        
        # each condition contains images to be quantified. Scan through each and run quantifying script
        for condition in experiment_conditions:

            cond_name = condition.split(os.sep)[-1]
            # check if user asked for condition to be ignored
            if cond_name in ignore:
                print("Ignoring condition: ", cond_name)
                continue

            # otherwise, continue with quantification
            print("**********")
            print("Now quantifying: ", cond_name)
            print("**********")

            # create a subdirectory to store annotated cell count images if one does not already exist
            directory = os.path.join(condition, "Cell Counts")
            if not os.path.exists(directory):
                os.makedirs(directory)

            # collect list of all tif files within each folder
            imgnames = [i for i in glob.glob(os.path.join(condition, "*.tif"))]
            imgnames.sort()

            # quantify cell counts and thresholds 
            raw_imgnames, final_cell_counts, thresholds = quantify.quantifyCells(imgnames)
            
            # output final cell counts and thresholds corresponding to each image into excel sheet
            d = {"File Name": raw_imgnames, "Cell Count": final_cell_counts, "Threshold": thresholds}
            df = pd.DataFrame(data = d)
            df.to_excel(writer, cond_name)
    
        writer.save()
        print("Done with Culture: ", culture_name)
        print()
    print("Done with Experiment: ", e_name)
