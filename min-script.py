import sys, subprocess, os, shutil
from pathlib import Path

#----------------Argument List Generation----------------#

# Returns template for computation minimisation
def full():

    return ['insert afl command', '-i', 'input', '-o', 'output', 'bigrapher', 'full', '-p', '/dev/null', '@@']


# Returns template for simulation minimisation
def sim():

    return ['insert afl command', '-i', 'input', '-o', 'output', 'bigrapher', 'sim', '-T', '500', '-s', '-t', '/dev/null', '-f', 'svg', '@@']


# Returns template for validation minimisation
def val():

    return ['insert afl command', '-i', 'input', "-o", 'output', 'bigrapher', 'validate', '-d', '/dev/null', '-f', 'svg', '@@']

#----------------Argument Parsing----------------#
# Note: terminal takes file call as argv[0]. Script is called "python3 min-script.py [option] input output"
mode = sys.argv[1]
input_dir = sys.argv[2]
output_dir = sys.argv[3]

# Calls relevant Bigrapher arguments
if(mode == 'full'):

    args_list = full()
elif(mode == 'sim'):

    args_list = sim()

elif(mode == 'val'):

    args_list = val()

else:

    print('invalid bigrapher flag please select on of the following: sim, full, val followed by input and output directory')

# Sets afl mode, input and output directories
# Note: directories are always the 2nd and 4th afl-cmin/tmin argument.
args_list[0] = 'afl-cmin'
args_list[2] = input_dir
args_list[4] = output_dir

#----------------Terminal Calls----------------#
# This will call af-cmin with input and output dir. If fails then will display an error message
# copy all files in input to output and will fail the script
subprocess.run(args_list, check=True)

# Creates an iterator object that will iterate all files in output_directory
corpus_files = os.listdir(output_dir)

# Initialises counter
i = 0

# Iterates through all files in newly minimised corupus and reduced them to the minimal number of usefull bits
for file in corpus_files:
    # Increments counter
    i += 1
    # Prints test number current-test/total-tests
    print('minimising ' + str(i) + '/' + str(len(corpus_files)) + '\n')

    #Creates path to file
    seed = (str(output_dir) + '/' + str(file))
    # Sets minimistation tool, input and output files
    args_list[0] = 'afl-tmin'
    args_list[2] = seed
    args_list[4] = seed
    # Calls afl-tmin
    subprocess.run(args_list)



    