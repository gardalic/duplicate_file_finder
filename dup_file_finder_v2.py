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
        self.start_dir = start_dir
        self.output_loc = output_loc
        self.all_files = {}
        self.extension = extension

    def find_files(self):
        """
            Lists out all files, creates a dictionary of unique file names with a list off all parent 
            folders it found the file.
        """
        print("Starting search...")
        for root, subdir, file in os.walk(self.start_dir):
            for f in file:
                # remove empty and check extension
                if f and f.endswith(self.extension):
                    # Init key if it doesn't exist
                    if not self.all_files.get(f):
                        self.all_files[f] = []
                    self.all_files[f].append(os.path.abspath(root))
        print(f"Processing finished, listed all files in {self.start_dir}")

    def keep_dupes(self):
        """ Method that goes through the list and pops the files that have a single parent. Split off
        from find_files so find_files can be used alone. """
        counter = 0  # just for the print, not really needed
        file_names = [name for name in self.all_files.keys()]
        for name in file_names:
            if len(self.all_files[name]) == 1:
                self.all_files.pop(name)
            else:
                # it won't count the original
                counter += len(self.all_files[name]) - 1

        print(f"Processing finished, found {counter} duplicates")

    def build_output(self):
        """
            Overwrites the file at the location specified by output_loc (default: where the script was run 
            from). The delimiter is set to ','. 
        """
        if self.all_files:
            err_list = []
            try:
                with open(os.path.join(self.output_loc, 'file_list.csv'), 'w', encoding='utf-8') as f:
                    for k, v in self.all_files.items():
                        for pth in v:
                            # Format with delimiter and line terminator
                            f.write(f"{k},{pth}\n")
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
    ext = input("Enter extension (if not looking for an extension, skip): ")

    df = FindDupes(start_loc, out_loc, ext)
    df.find_files()
    df.keep_dupes()
    df.build_output()
