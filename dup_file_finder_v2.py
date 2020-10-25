import os
# import pdb


class FindDupes:
    """
        List out files on a location and create a list duplicate files (by name) and their path.
        Version 2 - thought using dictionaries might make it simpler and more efficient
    """

    def __init__(self, start_dir=os.getcwd(), output_loc=os.getcwd(), extension=''):
        """
            If start_dir is omited it will use the directory the script is run from. If output_loc is
            omitted, it will generate 'file_list.csv' in the same location.
        """
        # TODO when you see it works, add extension option
        self.start_dir = start_dir
        self.output_loc = output_loc
        self.all_files = {}
        self.extension = extension

    def find_files(self):
        """
            Lists out all files, creates a dictionary of unique file names with a list off all parent folders 
            it found the file. It then goes through the list and pops the files that have a snigle parent
        """
        print("Starting search...")
        for root, subdir, file in os.walk(self.start_dir):
            for f in file:
                # init key if one doesn't exist
                if not self.all_files.get(f):
                    self.all_files[f] = []
                if f and f.endswith(self.extension):  # remove empty
                    self.all_files[f].append(root)

        counter = 0  # just for the print, not really needed
        working_dict = {key: value for (key, value) in self.all_files.items()}
        for k in working_dict:
            if len(working_dict[k]) == 1:
                self.all_files.pop(k)
            else:
                # it won't count the original
                counter += len(working_dict[k]) - 1

        print(f"Processing finished, found {counter} duplicates")

    def build_output(self):
        """
            Overwrites the file at the location specified by output_loc (default: where the script was run from). The delimiter is set to ','. 
        """
        if self.all_files:
            err_list = []
            with open(os.path.join(self.output_loc, 'file_list.csv'), 'w') as f:
                try:
                    for k, v in self.all_files.items():
                        try:
                            for pth in v:
                                # Format with delimiter and line terminator
                                f.write(f"{k},{pth}\n")
                        except UnicodeEncodeError:
                            err_list.append(f"{k},{pth}")
                    if err_list:
                        with open(os.path.join(self.output_loc, 'file_list_err.csv'), 'w', encoding='utf-8') as ef:
                            for line in err_list:
                                ef.write(f"{line}\n")
                    print(
                        f"Finished writing file, file location: {self.output_loc}")
                except IOError:
                    print(f"Couldn't create file at {self.output_loc}")
                    raise IOError
        else:
            print("No duplicates found...")


if __name__ == '__main__':
    # TODO incorporate argparse
    start_loc = input("Enter the starting location for the search: ")
    out_loc = input("Enter the output location for the CSV: ")

    df = FindDupes(start_loc, out_loc)
    df.find_files()
    df.build_output()
