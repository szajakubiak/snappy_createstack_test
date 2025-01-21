import os

HOME_PATH = os.path.expanduser("~")
SNAP_PYTHON_PATH = os.path.join(HOME_PATH, ".snap", "snap-python")

import sys

sys.path.append(SNAP_PYTHON_PATH)

import esa_snappy
import glob


DATA_PATH = "data"
REFERENCE_DATE = "20190429"
OUTPUT_FILE_NAME = "stack_file_script.dim"


# Get list of files
files = glob.glob(DATA_PATH + "\*.dim")
files.sort()
# Put reference file as the first one in the list
files_reordered = [ref for ref in files if REFERENCE_DATE in ref] + [file for file in files if REFERENCE_DATE not in file]
# Append working directory to file path to match SNAP Desktop behaviour
files_reordered = [os.path.join(os.getcwd(), file) for file in files_reordered]


# Read the reference file
parameters = esa_snappy.HashMap()
parameters.put("useAdvancedOptions", "false")
parameters.put("file", files_reordered[0])
parameters.put("formatName", "BEAM-DIMAP")
parameters.put("copyMetadata", "true")
stacked_product = esa_snappy.GPF.createProduct("Read", parameters)
del parameters


# Add files to the stack in a loop
for new_file in files_reordered[1:]:
    # Read next file
    parameters = esa_snappy.HashMap()
    parameters.put("useAdvancedOptions", "false")
    parameters.put("file", new_file)
    parameters.put("formatName", "BEAM-DIMAP")
    parameters.put("copyMetadata", "true")
    new_product = esa_snappy.GPF.createProduct("Read", parameters)
    del parameters
    
    # Add new file to the stack
    parameters = esa_snappy.HashMap()
    parameters.put("resamplingType", "NEAREST_NEIGHBOUR")
    parameters.put("initialOffsetMethod", "Orbit")
    parameters.put("extent", "Master")
    stacked_product = esa_snappy.GPF.createProduct("CreateStack", parameters, [new_product, stacked_product])
    del parameters


# Export stack to the file
file_name = os.path.join(os.getcwd(), OUTPUT_FILE_NAME)
parameters = esa_snappy.HashMap()
parameters.put("writeEntireTileRows", "false")
parameters.put("file", file_name)
parameters.put("deleteOutputOnFailure", "true")
parameters.put("formatName", "BEAM-DIMAP")
parameters.put("clearCacheAfterRowWrite", "false")
stack_data = esa_snappy.GPF.createProduct("Write", parameters, stacked_product)
