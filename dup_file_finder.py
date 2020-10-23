import os
from collections import Counter
# import pdb


class FindDupes:
    """
        List out files on a location and create a list duplicate files (by name) and their path.
    """

    def __init__(self, start_dir=os.getcwd()):
        """
            If start_dir is omited it will use the directory the script is run from. If output_loc is omitted, it will generate 'file_list.csv' in the same location.
        """
        # TODO when you see it works, add extension option
        self.start_dir = start_dir
        self.duplicates = []

    def find_duplicates(self):
        """
            List out all files, create a list of duplicates.
        """
        all_files = []
        print("Starting search...")
        for root, subdir, file in os.walk(self.start_dir):
            for f in file:
                all_files.append([root, f])

        files_count = Counter([file[1] for file in all_files])

        self.duplicates = [
            file for file in all_files if files_count[file[1]] > 1]

        print(f"Processing finished, found {len(self.duplicates)} duplicates")

    def build_file(self, lst, output_loc=os.getcwd()):
        """
            Overwrites the file at the location specified by output_loc (default: where the script was run from). The delimiter is set to ','. 
        """
        if len(lst) > 0:
            save_path = os.path.join(output_loc, 'file_list.csv')
            err_list = []
            with open(save_path, 'w') as f:
                try:
                    for file in lst:
                        try:
                            # Format with delimiter and line terminator
                            f.write(f"{file[0]},{file[1]}\n")
                        except UnicodeEncodeError:
                            err_list.append(f"{file[0]},{file[1]}")
                    if err_list:
                        with open(os.path.join(output_loc, 'file_list_err.csv'), 'w', encoding='utf-8') as ef:
                            for line in err_list:
                                ef.write(f"{line}\n")
                    print(f"Finished writing file, file location: {save_path}")
                except IOError:
                    print(f"Couldn't create file at {save_path}")
                    raise IOError
        else:
            print("List is empty...")


if __name__ == '__main__':
    # TODO incorporate argparse
    start_loc = input("Enter the starting location for the search: ")
    out_loc = input("Enter the output location for the CSV: ")

    df = FindDupes(start_loc)
    df.find_duplicates()
    df.build_file(df.duplicates, out_loc)
