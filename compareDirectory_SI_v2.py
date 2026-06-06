import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

'''
Script to compare two directories and the files within them to determine inconsistencies. 
Select two folders and let the magic take place. 

By Erick Begishev '27
June. 2026
Version 2.0

Designed for UR Baja SAE Systems Integration
'''

OUTPUT_FILE = "comparison_results.txt"


def get_file_info(directory):
    """
    Returns dictionary:
    {
        filename: modification_time
    }
    """
    file_info = {}

    for root, _, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)

            try:
                modified_time = os.path.getmtime(full_path)
                file_info[file] = modified_time
            except OSError:
                pass

    return file_info


def write_output(text, file_handle):
    print(text)
    file_handle.write(text + '\n')


def compare_folders():
    root = tk.Tk()
    root.withdraw()

    print("Select first folder")
    folder1 = filedialog.askdirectory(title="Select First Folder")

    if not folder1:
        return

    print("Select second folder")
    folder2 = filedialog.askdirectory(title="Select Second Folder")

    if not folder2:
        return

    # Options window
    options_window = tk.Toplevel()
    options_window.title("Export Options")

    export_folder1_only = tk.BooleanVar(value=True)
    export_folder2_only = tk.BooleanVar(value=True)
    export_same_files = tk.BooleanVar(value=False)
    export_same_name_diff_date = tk.BooleanVar(value=True)

    tk.Checkbutton(
        options_window,
        text="Files only in first folder",
        variable=export_folder1_only
    ).pack(anchor="w", padx=10)

    tk.Checkbutton(
        options_window,
        text="Files only in second folder",
        variable=export_folder2_only
    ).pack(anchor="w", padx=10)

    tk.Checkbutton(
        options_window,
        text="Same files (same modified date)",
        variable=export_same_files
    ).pack(anchor="w", padx=10)

    tk.Checkbutton(
        options_window,
        text="Same name but different modified date",
        variable=export_same_name_diff_date
    ).pack(anchor="w", padx=10)

    confirmed = tk.BooleanVar(value=False)

    def submit():
        confirmed.set(True)
        options_window.destroy()

    tk.Button(options_window, text="Compare", command=submit).pack(pady=10)

    options_window.wait_window()

    if not confirmed.get():
        return

    folder1_name = os.path.basename(folder1)
    folder2_name = os.path.basename(folder2)

    files1 = get_file_info(folder1)
    files2 = get_file_info(folder2)

    names1 = set(files1.keys())
    names2 = set(files2.keys())

    only_in_folder1 = names1 - names2
    only_in_folder2 = names2 - names1

    common_files = names1 & names2

    same_files = []
    different_dates = []

    for filename in common_files:
        time1 = files1[filename]
        time2 = files2[filename]

        if time1 == time2:
            same_files.append(filename)
        else:
            different_dates.append(
                (
                    filename,
                    datetime.fromtimestamp(time1),
                    datetime.fromtimestamp(time2)
                )
            )

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as output_file:

        write_output("Comparison Results", output_file)
        write_output("=" * 50, output_file)

        if export_folder1_only.get():
            write_output(
                f"\nFiles only in {folder1_name}:",
                output_file
            )

            if only_in_folder1:
                for file in sorted(only_in_folder1):
                    write_output(file, output_file)
            else:
                write_output("None", output_file)

        if export_folder2_only.get():
            write_output(
                f"\nFiles only in {folder2_name}:",
                output_file
            )

            if only_in_folder2:
                for file in sorted(only_in_folder2):
                    write_output(file, output_file)
            else:
                write_output("None", output_file)

        if export_same_files.get():
            write_output(
                "\nFiles with same name and same modified date:",
                output_file
            )

            if same_files:
                for file in sorted(same_files):
                    write_output(file, output_file)
            else:
                write_output("None", output_file)

        if export_same_name_diff_date.get():
            write_output(
                "\nFiles with same name but different modified dates:",
                output_file
            )

            if different_dates:
                for file, date1, date2 in sorted(different_dates):
                    write_output(
                        f"{file}\n"
                        f"    Folder 1: {date1}\n"
                        f"    Folder 2: {date2}",
                        output_file
                    )
            else:
                write_output("None", output_file)

    messagebox.showinfo(
        "Finished",
        f"Results saved to:\n{OUTPUT_FILE}"
    )


if __name__ == "__main__":
    compare_folders()