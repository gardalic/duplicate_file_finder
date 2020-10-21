import os
import sys
from collections import Counter


class FindDupes:
    """
        List out files on a location and create a list duplicate files (by name) and their path.
    """

    def __init__(self, start_dir=None, output_file=None):
        """
            If start_dir is omited it will use the directory the script is run from. If output_file is omitted, it will generate 'file_list.csv' in the same location.
        """
        # TODO when you see it works, add extension option
        self.start_dir = start_dir
        self.output_file = output_file
        self.duplicates = []

    def find_duplicates(self):
        """
            List out all files, create a list of duplicates.
        """
        all_files = []
        print("Starting search...")
        for root, subdir, file in os.walk(self.start_dir):
            for f in file:
                all_files.append([file, os.path.join(root, f)])

        files_count = Counter([file[0] for file in all_files])
        print(f"Found {len(files_count)} unique files...")

        self.duplicates = [file for file in all_files if files_count[file[0]] > 1]
        print(f"Processing finished, found {len(self.duplicates)} duplicates")

    def build_file(self, dup_list):
        """
            Overwrites the file at the location specified by output_file (default: where the script was run from). The delimiter is set to ','. 
        """
        if len(dup_list) > 0:
            with open(self.output_file, 'w') as f:
                try:
                    f.writelines((f"{file[0]},{file[1]}\n" for file in dup_list)) # Format with delimiter and line terminator
                except IOError:
                    print(f"Couldn't create file ")
