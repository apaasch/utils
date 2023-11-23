import argparse
import ROOT

def print_branches_for_keys(input_file, keys_of_interest, ttree_name):
    # Open the input file
    root_file = ROOT.TFile(input_file)

    # Check if the file is open and readable
    if not root_file or root_file.IsZombie():
        print("Error opening file:", input_file)
        return
    
    # Get the TTree from the ROOT file
    ttree = root_file.Get(ttree_name)

    # Get the list of keys in the ROOT file
    key_list = root_file.GetListOfKeys()

    # Check if the TTree exists and is readable
    if not ttree:
        print("Error opening TTree:", ttree_name)
        return

    # Get the list of keys (branches) in the TTree
    branch_list = ttree.GetListOfBranches()

    # Check if the TTree has branches
    if len(branch_list) == 0:
        print("Error reading Branches for TTree", ttree_name, ": List of branches has no entries")
        return

    # Loop over the keys of interest
    for key_name in keys_of_interest:
        # Flag to check if the key is found
        key_found = False

        # Loop over all keys in the file
        if not key_name in branch_list:
            print("Error: Key not found -", key_name)
            print("Available keys:")
            for key in branch_list:
                print("- ", key.GetName())
        
        # Get the specified branch from the TTree
        branch = ttree.GetBranch(key_name)
        print(branch)
        
        # Get the list of leaves in the branch
        branch_list = branch.GetListOfBranches()

        # Check if the branch has leaves
        if len(branch_list) == 0:
            print("Error reading Leaves for Branch", branch_name, ": List of leaves has no entries")
            return

        # Print the branch and its leaves
        print("Branch:", key_name)
        print("Leaves:")
        for leaf in branch_list:
            leaf_name = leaf.GetName()
            print("- ", leaf_name)

    # Close the ROOT file
    root_file.Close()

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Print branches for specific keys in a ROOT file.")
parser.add_argument("-i", "--input-file", dest="input_file", help="Path to the input ROOT file")
parser.add_argument('-k', '--keys-of-interest', nargs='+', dest='keys_of_interest', help='List of keys to print branches for')
parser.add_argument('-t', '--ttree', default='AnalysisTree', dest='ttree_name', help='Name of the TTree to print branches for')
args = parser.parse_args()

# Call the function with the input file and keys of interest provided
print_branches_for_keys(args.input_file, args.keys_of_interest, args.ttree_name)
