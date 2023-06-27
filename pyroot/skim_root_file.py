import argparse
import ROOT
from array import array

def skim_root_file(input_file, output_file, keep_leafs, debug):
    # Open the input file
    input_file = ROOT.TFile(input_file)

    # Check if the file is open and readable
    if not input_file or input_file.IsZombie():
        print("Error opening file:", input_file)
        return

    # Get the AnalysisTree TTree from the input file
    input_tree = input_file.Get("AnalysisTree")

    # Create a new output file
    output_file = ROOT.TFile(output_file, "RECREATE")

    # Create a new output tree with the same name
    output_tree = ROOT.TTree("AnalysisTree", "Analysis Tree")

    # Create a dictionary to hold the variables for each TLeaf
    leaf_vars = {}

    # Loop over the TLeafs to keep and create corresponding variables
    for leaf_name in keep_leafs:
        if debug: print("Adding leaf:", leaf_name)
        leaf_var = array('f', [0.0])
        leaf_vars[leaf_name] = leaf_var
        output_tree.Branch(leaf_name, leaf_var, leaf_name+'/F')

        # Get the TLeaf from the input tree
        leaf = input_tree.GetLeaf(leaf_name)

        # Set the branch address for the TLeaf in the input tree
        input_tree.SetBranchAddress(leaf_name, leaf_var)


    # Loop over the entries in the input tree and fill the output tree
    if debug: print("Processing events")

    for ievent in range(input_tree.GetEntries()):
        input_tree.GetEntry(ievent)

        # Fill the output tree with the values of the kept TLeafs
        for leaf_name, leaf_var in leaf_vars.items():
            leaf = input_tree.GetLeaf(leaf_name)
            leaf_val = leaf.GetValue()
            leaf_var[0] = leaf_val

        output_tree.Fill()
    if debug: print("Finishing events")

    # Write the output tree to the output file
    output_file.Write()

    # Close the input and output files
    input_file.Close()
    output_file.Close()

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Skim ROOT file by extracting specific TLeafs to a new TTree.")
parser.add_argument("-i", "--input-file", dest="input_file", help="Path to the input ROOT file")
parser.add_argument("-o", "--output-file", dest="output_file", help="Path to the output ROOT file")
parser.add_argument(      "--debug", dest="debug", action="store_true", help="Enable debug mode")
parser.add_argument("-k", "--keep-leafs", dest="keep_leafs", nargs="+", default=["pt_sub1_rec"], help="List of TLeafs to keep in the output TTree")
args = parser.parse_args()

if args.debug:
    print("Input file:", args.input_file)
    print("Output file:", args.output_file)
    print("Keep leafs:", args.keep_leafs)
    print("Debug:", args.debug)

# Call the function with the input and output files, the list of TLeafs to keep, and the debug flag
skim_root_file(args.input_file, args.output_file, args.keep_leafs, args.debug)