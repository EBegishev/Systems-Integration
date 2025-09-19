import os
from tkinter import filedialog, Tk

'''
Script to compare two directories and the files within them to determine inconsistencies. 
Select two folders and let the magic take place. 

By Erick Begishev '27
Sep. 2025
Version 1.1

Designed for UR Baja SAE Systems Integration
'''

OUTPUT_FILE = "comparison_results.txt"

def get_file_names(directory): #get file names from directory
    file_names = set()
    for root, _, files in os.walk(directory):
        for file in files:
            file_names.add(file)
    return file_names

def write_output(text, file_handle):
    print(text)
    file_handle.write(text + '\n')

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
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as output_file:
        write_output("\nResults:", output_file)

        if only_in_folder1:
            write_output(f"{folder1_name} has but {folder2_name} doesn't:", output_file)
            for file in sorted(only_in_folder1):
                write_output(file, output_file)

        if only_in_folder2:
            write_output(f"{folder2_name} has but {folder1_name} doesn't:", output_file)
            for file in sorted(only_in_folder2):
                write_output(file, output_file)

        if not only_in_folder1 and not only_in_folder2:
            write_output(f"Both {folder1_name} and {folder2_name} have the same file names", output_file)

    print(f"\nResults also written to: {OUTPUT_FILE}")

compare_folders()
