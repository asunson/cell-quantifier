# User Guide

This package was written for use by the Skobe Lab at the Icahn School of Medicine 

Hello! We all know that the current process of cell quantification is unnecessarily complicated. Right now, we need to keep switching between an excel sheet and the imaging program, deal with the fact that it doesn't switch screens properly, individually load each set of images for each experimental condition, manually adjust for background noise, eyeball how many cells were missed or how many to exclude, and so on...

The point of this program is to try and help make your life a little easier. All you need to do is feed the program a path to the experiment folder and it will move through all the folders and present you the images one after another to quantify until you finish them all. No need to leave the screen!

After you're done, it will drop a nice excel sheet called "Quantification Results.xlsx" containing the cell count for each image and threshold used. Each sheet in the workbook is specific to an experimental condition. One Excel book will be created for each culture (ex. LECs and no LECs). 

**Note:** The Quantification Results excel sheet is easily overwritten, it is recommended to move the data to another file immediately upon program completion. 

Right now this program makes the following key assumption about the folder layout based on how the directory is currently organized:

                            ---------------
                            | Exp. Number | <--- Folder (path to this folder should be given to the program)
                            ---------------
                              /        \
                             /          \
                        --------    -----------
                        | LECs |    | No LECs | <--- Folders
                        --------    -----------
                         /                  \ 
        ---------------------------   ---------------------------
        | Experimental Conditions |   | Experimental Conditions | <--- Folders containing images
        ---------------------------   ---------------------------
         |  |  |  |  |  |  |  |  |     |  |  |  |  |  |  |  |  |  
        ---------------------------   --------------------------- 
        |         Images          |   |         Images          | <--- Images 
        ---------------------------   --------------------------- 

---

# How to Use

Provide the path to the experiment folder in the file "paths.txt". Please put each path on a separate line. 

Windows uses backslashes ("\\") whereas Macs use foward slashes ("/")

Then, making sure that python is properly installed, double click the shortcut labeled `cell quantifier`. It will open up a command prompt to run the program. 

The program should start up and display the first image to be quantified. Initially, it will detect as many cells as possible based on the default threshold and minimum area values. Manual controls can be used to modify values and add/remove cells. 

If you would like to exit early, make sure you close out of the command prompt rather than the image window. 

---

# Features and Controls

## Features

There are a few built in features to make quantifying cells easier. 

Threshold and Minimum Area bars: threshold and min area values can be modified by sliding the corresponding bars. The default values for threshold and min area are 40 and 35 respectively. Minimum area is in pixels so the conversion from pixel to real life measurement should be calculated. 

The user has the ability to provide the program with a list of conditions to ignore (skip quantification) in `ignore.txt`.

## Controls

* Left click =  Add a cell. This draws a blue circle on the image and increments the total cell count.

* Right click = Remove a cell. This draws a red X on the image and decrements the total cell count.

* "A" = Debugging information. Will print the current cell count, threshold, and min area in the command prompt. 

* "R" = Reset. Resets the image to default values and erases and marks. 

* "Z" = Undo. Undoes the last action.

* Enter = Done. Marks the image as complete, writes the total cell count onto the image, saves it, and loads the next in the series. 

## Future Features

Things I should implement in the future:

* A way to quantify just one experiment at a time

* Make gaussian blur modifiable

* Early exit feature (other than x'ing out of the command prompt or giving a keyboard interrupt)

* Method to differentiate between the same condition within different cultures while ignoring

* Ability to zoom in on an image



