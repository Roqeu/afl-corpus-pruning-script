# Used to get directory locations, target program and Bigrapher Mode
from sys import argv
# Used to call afl-cmin and create new terminals
from subprocess import Popen, run
# Used to move files to new directory
from shutil import move
# Used to handle directory content, path and deletion when finished
from os import listdir, mkdir, path
# Used to get number of cores on machine
import multiprocessing as mp
# Used to wait between tmin-script checks
from time import sleep

# Represents if completed mode should call next mode in sequence of calls or stop
complete_run = True

# ----------------Directory creation and tmin-script activation----------------#
# Splits large corpus into smaller directories and returns a list of new directories
def split_corpus(corpus_dir):
    ### Splits up files into smaller directories for tmin-script ###
    # Creates an list of all files in the corpus directory
    corpus_files = listdir(corpus_dir)
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
        new_dir = path.join(corpus_dir, 'tmin' + str(i))
        mkdir(new_dir)
        # Adds new directory to directory list
        dir_list.append(new_dir)

        # Moves fraction of files (no_of_seeds or number of remaining files) into new directory
        for i in range(0, min(no_of_seeds, len(corpus_files))):

            # Creates a path to move the seed file to and removes seed file from list
            old_dir = path.join(corpus_dir, corpus_files.pop())
            # Moves the seed file
            move(old_dir, new_dir)
    
    return dir_list

# Splits Corpus into smaller directories and starts test minimisation
def minimise_tests(corpus_dir, mode):

    # Splits up main corpus dirtectory into smaller directories and stores list of new directories
    dir_list = split_corpus(corpus_dir)
    # Stores a list of running terminals
    running_procs = []
    
    # Opens new terminal window to run tmin script
    # Note: new terminals opened as tmin runs 1 process per terminal and will use 1 core per process 
    # (this how the script acheives asynchronus tmin operations)
    for d in dir_list:
        # Calls tmin script with relevant bigrapher mode
        # Note: subprocess.call is used instead of subprocess.run to allow the script to control the creation of new terminals
        running_procs.append(Popen(['gnome-terminal', '-e', 'python3 /home/r0qu3/tmin-script.py ' + corpus_dir + ' ' + d  + ' ' + target + mode]))

    return running_procs

            
# ----------------Bigrapher arguments for each mode----------------#
# Returns template for computation minimisation
def full(input_dir, output_dir, target):

    print('Starting full_corpus minimisation')
    # Sets path to full_corpus in input_directory
    input_corpus = path.join(input_dir, 'full_corpus')
    # Sets path to full_corpus in output_directory
    output_corpus = path.join(output_dir, 'full_corpus')
    # If file doesn't exist create it
    try:
        mkdir(output_corpus)
    # If file exists ask user to delete it and exit script
    except:
        print('Directory full_corpus exists, please delete it.')
        return

    # Minimised corpus size to minimum number of relevant files
    run(['afl-cmin', '-m', '500',  '-i', input_corpus, '-o', output_corpus, target, 'full', '-p', '/dev/null', '@@'], check=True)
    # Starts tmin process
    running_procs = minimise_tests(output_corpus, ' full')

    # If user did not select to only run 1 mode, call next function in sequence when current tmin is finished
    if complete_run:

        # Won't allow method to finish until all tmin-script processes are finished
        while len(running_procs) != 0:
            # Waits 5 minutes then checks running process to find complete minimisation scripts
            sleep(20)
            # Loops through processes in running_processes list
            for proc in running_procs:
                # If process is finished, remove from list
                if proc.poll is not None: # If process is running .poll should return None

                    running_procs.remove(proc)

        print('full_corpus minimisation complete! Have a nice day! :)')
        sim(input_dir, output_dir, target)
    else:

        print('full_corpus minimisation complete! Have a nice day! :)')

# Returns template for simulation minimisation
def sim(input_dir, output_dir, target):

    print('Starting sim_corpus minimisation')
    # Sets path to sim_corpus in input_directory
    input_corpus = path.join(input_dir, 'sim_corpus')
    # Sets path to sim_corpus in output_directory and creates it
    output_corpus = path.join(output_dir, 'sim_corpus')
    # If file doesn't exist create it
    try:
        mkdir(output_corpus)
    # If file exists ask user to delete it and exit script
    except:
        print('Directory sim_corpus exists, please delete it.')
        return

    # Minimised corpus size to minimum number of relevant files
    run(['afl-cmin', '-m', '500', '-i', input_corpus, '-o', output_corpus, target, 'sim', '-T', '500', '-s', '-t', '/dev/null', '-f', 'svg', '@@'], check=True)
    # Starts tmin process
    running_procs = minimise_tests(output_corpus, ' sim')

    # If user did not select to only run 1 mode, call next function in sequence when current tmin is finished
    if complete_run:

        # Won't allow method to finish untill all tmin-script processes are finished
        while running_procs:
            # Waits 5 minutes then checks running process to find complete minimisation scripts
            sleep(20)
            # Loops through processes in running_processes list
            for proc in running_procs:
                # If process is finished, remove from list
                if proc.poll is not None: # If process is running .poll should return None

                    running_procs.remove(proc)

        print('sim_corpus minimisation complete! Have a nice day! :)')
        validate(input_dir, output_dir, target)
    else:
        print('sim_corpus minimisation complete! Have a nice day! :)')

# Returns template for validation minimisation
def validate(input_dir, output_dir, target):

    print('Starting validate_corpus minimisation')
    # Sets path to validate_corpus in input_directory
    input_corpus = path.join(input_dir, 'validate_corpus')
    # Sets path to validate_corpus in output_directory and creates it
    output_corpus = path.join(output_dir, 'validate_corpus')
    # If file doesn't exist create it
    try:
        mkdir(output_corpus)
    # If file exists ask user to delete it and exit script
    except:
        print('Directory validate_corpus exists, please delete it.')
        return

    # Minimised corpus size to minimum number of relevant files
    run(['afl-cmin', '-m', '500', '-i', input_corpus, '-o', output_corpus, target, 'validate', '-d', '/dev/null', '-f', 'svg', '@@'], check=True)
    # Starts tmin process
    minimise_tests(output_corpus, ' validate')
    print('validate_corpus minimisation complete! Have a nice day! :)')


# ----------------Argument Parsing----------------#
# Note: terminal takes script call as argv[0]: "python3 min-script.py input output [bigrapher-mode] [tmin-option]"
args_len = len(argv)

# If not enough information passed to program, warn user and exit
if (args_len < 4):

    print("Invalid input. Script needs an input directory, an output directory and the executables location.")
else:

    # Input and output directories for pruning
    input_dir = argv[1]
    output_dir = argv[2]
    # Stores the location of instrumented .exe
    target = argv[3]
    # 5th argument always bigrapher mode
    if args_len == 5:
        # Tells function called not to call next function in call sequence
        complete_run = False
        # Sets bigrapher mode
        mode = argv[4]
        # Checks for and calls cmin function for relevant Bigrapher mode
        if (mode == 'full'):

            full(input_dir, output_dir, target, mode)
        elif (mode == 'sim'):

            sim(input_dir, output_dir, target)
        elif (mode == 'validate'):

            validate(input_dir, output_dir, target)
        else:

            print('Invalid bigrapher flag please select on of the following: sim, full, val followed by input and output directory')
    
    # Otherwise call the first function in the call sequence
    else:

        full(input_dir, output_dir, target)
        