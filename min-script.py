import sys, subprocess, os, shutil
import multiprocessing as mp
from pathlib import Path

# ----------------Terminal calls for each Bigrapher argument----------------#

# Set to True if tmin only enabled
tmin_mode = False


def start(input_dir, output_dir, mode):

    # Assume 5 arguments passed only when running tmin on 1 bigrapher mode
    # if args_len == 5:
    #   if sys.argv[4] == 'tmin':

    # Checks which bigrapher mode to run
    if args_len == 4:

        # Checks for and calls relevant Bigrapher arguments
        if (mode == 'full'):

            full(input_dir, output_dir)
        elif (mode == 'sim'):

            args_list = sim('afl-cmin', input_dir, output_dir)
        elif (mode == 'validate'):

            args_list = validate('afl-cmin', input_dir, output_dir)
        else:

            print('invalid bigrapher flag please select on of the following: sim, full, val followed by input and output directory')




# Returns template for computation minimisation
def full(input, output):
    # if(tmin_mode == False):

    #     subprocess.run(['afl-cmin', '-i', input, '-o', output, 'bigrapher', 'full', '-p', '/dev/null', '@@'], check=True)


    ### Splits up files into smaller directories for tmin-script

    # Creates an list of all files in output_directory
    corpus_files = os.listdir(output)
    # Stores number of threads to be made (will use all cores on CPU)
    threads = mp.cpu_count()

    # Stores the number of files to be stored each sub directory
    n = len(corpus_files) / threads
    # Converts n to int
    no_of_seeds = int(n)
    # If n is a decimal, add 1 to no_of_seeds so there are no remaining files
    # Note: this means there will be less files in the last directory so that all files are included
    if n != no_of_seeds:
        no_of_seeds += 1
    # Creates a list to store all new directories
    dir_list = []

    # Creates a directory per thread
    for i in range(0, threads):

        # Creates new directory
        new_dir = os.path.join(output, 'full' + str(i))
        os.mkdir(new_dir)
        dir_list.append(new_dir)

        # Moves fraction(no_of_seeds) of files into new directory
        for i in range(0, min(no_of_seeds, len(corpus_files))):
            old_dir = os.path.join(output, corpus_files.pop())
            shutil.move(old_dir, new_dir)

    for d in dir_list:


        subprocess.call(['gnome-terminal', '-e', 'python3 /home/r0qu3/tmin-script.py ' + d  + ' full'])

    # running_procs = [subprocess.Popen(['gnome-terminal -e bash python3 /home/r0qu3/tmin-script.py ' + str(d)], shell=True) for d in dir_list]

    # while running_procs:
    #     for proc in running_procs:

    #         returncode = proc.poll()
    #         if returncode is not None:
    #             running_procs.remove(proc)
    #             print("Process " + str(proc.pid) + " is finished!")
    #             break


# Returns template for simulation minimisation
# def siminput, output):

# return [mode, '-i', input, '-o', output, 'bigrapher', 'sim', '-T', '500', '-s', '-t', '/dev/null', '-f', 'svg', '@@']


# Returns template for validation minimisation
# def validate(input, output):

# return [mode, '-i', input, '-o', output, 'bigrapher', 'validate', '-d', '/dev/null', '-f', 'svg', '@@']

# ----------------Argument Parsing----------------#

# Note: terminal takes script call as argv[0]: "python3 min-script.py input output [bigrapher-mode] [tmin-option]"
args_len = len(sys.argv)

if (args_len != 4):

    print("Invalid input. Script needs an input and output directory.")
else:

    # Input and output directories for pruning
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    # Sets bigrapher mode
    mode = sys.argv[3]
    start(input_dir, output_dir, mode)