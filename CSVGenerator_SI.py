import os
import csv
from tkinter import filedialog, Tk

'''
Script to generate a CSV file containing all the file names within a selected folder.  
Select a folder and let the magic take place. 
CSV is saved to the same folder the program will run from. 

Make sure that file_names csv doesn't exist in the folder beforehand as it will overwrite it

By Erick Begishev '27
Feb. 2025
Version 1.1

Designed for UR Baja SAE Systems Integration
'''

#Tkinter root window
root = Tk()
root.withdraw()

#folder selection dialog
folder_path = filedialog.askdirectory(title="Select a folder")

#check if a folder was selected 
if not folder_path:
    print("No folder selected. Program terminated.")
else:
    #get file names from the selected folder
    file_names = os.listdir(folder_path)

    #file path for the CSV file
    csv_file_path = os.path.join(folder_path, 'file_names.csv')

    #create and write to CSV file
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        #write each file name to row
        for file_name in file_names:
            writer.writerow([file_name])

    print(f"CSV file 'file_names.csv' has been created with {len(file_names)} file names from {folder_path}")

root.destroy() #exit