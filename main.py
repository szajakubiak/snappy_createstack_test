import os

HOME_PATH = os.path.expanduser("~")
SNAP_PYTHON_PATH = os.path.join(HOME_PATH, ".snap", "snap-python")

import sys

sys.path.append(SNAP_PYTHON_PATH)

import esa_snappy
import glob


DATA_PATH = "data_mix_3"
REFERENCE_DATE = "20190429"
OUTPUT_FILE_NAME = "stack_file_script.dim"


files = glob.glob(DATA_PATH + "\*.dim")
files.sort()
# Put reference file as the last one in list
files_reordered = [file for file in files if REFERENCE_DATE not in file] + [ref for ref in files if REFERENCE_DATE in ref]
# Append working directory to file path to match SNAP Desktop behaviour
files_reordered = [os.path.join(os.getcwd(), file) for file in files_reordered]

products = []
print("Files order:")
for file in files_reordered:
    parameters = esa_snappy.HashMap()
    parameters.put("useAdvancedOptions", "false")
    parameters.put("file", file)
    parameters.put("formatName", "BEAM-DIMAP")
    parameters.put("copyMetadata", "true")
    file_data = esa_snappy.GPF.createProduct("Read", parameters, products)
    products.append(file_data)
    print(f"{products[-1].getName()}")


parameters = esa_snappy.HashMap()
parameters.put("resamplingType", "NEAREST_NEIGHBOUR")
parameters.put("initialOffsetMethod", "Orbit")
parameters.put("extent", "Master")
stack_data = esa_snappy.GPF.createProduct("CreateStack", parameters, products)


file_name = os.path.join(os.getcwd(), OUTPUT_FILE_NAME)
parameters = esa_snappy.HashMap()
parameters.put("writeEntireTileRows", "false")
parameters.put("file", file_name)
parameters.put("deleteOutputOnFailure", "true")
parameters.put("formatName", "BEAM-DIMAP")
parameters.put("clearCacheAfterRowWrite", "false")
stack_data = esa_snappy.GPF.createProduct("Write", parameters, stack_data)
