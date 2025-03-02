import os
from tkinter import filedialog, Tk

'''
Script to compare two directories and the files within them to determine inconsistencies. 
Select two folders and let the magic take place. 

By Erick Begishev '27
Feb. 2025
Version 1.0

Designed for UR Baja SAE Systems Integration
'''

def get_file_names(directory): #get file names from directory
    file_names = set()
    for root, _, files in os.walk(directory):
        for file in files:
            file_names.add(file)
    return file_names

def compare_folders(): #compare folders with file names
    root = Tk()
    root.withdraw()
    
    #select folders
    print("Select first folder")
    folder1 = filedialog.askdirectory(title="Select First Folder")
    
    print("Select second folder")
    folder2 = filedialog.askdirectory(title="Select Second Folder")
    
    #get folder names for display
    folder1_name = os.path.basename(folder1)
    folder2_name = os.path.basename(folder2)
    
    #get file names
    files1 = get_file_names(folder1)
    files2 = get_file_names(folder2)
    
    #find differences
    only_in_folder1 = files1 - files2
    only_in_folder2 = files2 - files1
    
    #print results
    print("\nResults:")
    if only_in_folder1:
        print(f"{folder1_name} has but {folder2_name} doesn't:")
        for file in sorted(only_in_folder1):
            print(file)
    
    if only_in_folder2:
        print(f"{folder2_name} has but {folder1_name} doesn't:")
        for file in sorted(only_in_folder2):
            print(file)
    
    if not only_in_folder1 and not only_in_folder2:
        print(f"Both {folder1_name} and {folder2_name} have the same file names")

compare_folders()