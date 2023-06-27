import argparse
import ROOT

def print_root_info(input_file):
    # Open the input file
    root_file = ROOT.TFile(input_file)

    # Check if the file is open and readable
    if not root_file or root_file.IsZombie():
        print("Error opening file:", input_file)
        return

    # Get the list of keys in the ROOT file
    key_list = root_file.GetListOfKeys()

    # Loop over the keys and print their information
    for key in key_list:
        key_name = key.GetName()
        key_class_name = key.GetClassName()
        print("Key:", key_name)
        print("Class Name:", key_class_name)

        # Check if the key is a TTree
        if key_class_name == "TTree":
            # Open the TTree
            ttree = root_file.Get(key_name)

            # Check if the TTree exists and is readable
            if not ttree:
                print("Error opening TTree:", key_name)
                continue

            # Get the list of branches in the TTree
            branch_list = ttree.GetListOfBranches()

            # Loop over the branches and print their names
            print("Branches:")
            for branch in branch_list:
                branch_name = branch.GetName()
                print("- ", branch_name)

        print("")

    # Close the ROOT file
    root_file.Close()

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Print information about keys, TTrees, and branches in a ROOT file.")
parser.add_argument("input_file", help="Path to the input ROOT file")
args = parser.parse_args()

# Call the function with the input file provided
print_root_info(args.input_file)

