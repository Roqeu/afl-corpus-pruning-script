# Used to call afl-tmin
from subprocess import run
# Used to copy minimised files back to parent directory
from shutil import move
# Used to get directory locations, target program and Bigrapher Mode
from sys import argv
# Used to handle directory content, path and deletion when finished
from os import listdir, scandir, path, rmdir

#---------------Handles moving files back to parent directory---------------#
# Note: afl expects 1 corpus directory of seed files, this function returns all minimised files to main corpus directory
def copy_back(corpus_directory, parent_directory):

     # Stores seed files as list instead of iterable as allows for easier path creation
    seed_files = listdir(corpus_directory)

    # Loops through corpus directory and copies 
    for seed in seed_files:

        # Creates path of file to be moved
        old_dir = path.join(corpus_directory, seed)
        # Moves file to main corpus directory
        move(old_dir, parent_directory)

    # Deletes now empty subdirectory
    rmdir(corpus_directory)

# Minimise every test case in directory
def minimise(corpus_directory, parent_directory, tmin_call):

    # Stores an iterator of DirEntry objects
    seed_files = scandir(corpus_directory)
    # Initialises counter
    i = 0          

    # Iterates through all files in directory and reduces them to the smallest number of useful bits
    for seed in seed_files:

        # Increments counter
        i += 1
        # Prints test number current-test/total-tests
        print('minimising ' + str(i) + '/' + str(total_files) + '\n')
        # Sets file to be minimised
        tmin_call[4] = seed
        tmin_call[6] = seed
        # Calls afl-tmin
        # Note: this is set up to overight existing seed file rather than create a copy
        run(tmin_call)

    # Moves all minimised seed files back to main corpus file    
    copy_back(corpus_directory, parent_directory)
    # Informs user of completion
    print('Tmin process completed! Have a nice day! :)')


#---------------Sets up tmin call for each mode---------------#
def full(target):  

    # Return tmin call for full mode
    return ['afl-tmin', '-m', '500', '-i', '', '-o', '', target, 'full', '-p', '/dev/null', '@@'])

def sim(target): 

    # Return tmin call for sim mode
    return ['afl-tmin', '-m', '500',  '-i', '', '-o', '', target, 'sim', '-T', '500', '-s', '-t', '/dev/null', '-f', 'svg', '@@']


def validate(target):  

    # Return tmin call for validate mode
    return ['afl-tmin', '-m', '500',  '-i', '', '-o', '', target, 'validate', '-d', '/dev/null', '-f', 'svg', '@@']



#---------------Parsing input---------------#
# Stores the location of the parent directory to copy minimised files to
parent_directory = argv[1]
# Stores the location of the corpus_directory
corpus_directory = argv[2]
# Stores location of target .exe
target = argv[3]
# Stores the bigrapher mode to be tested
mode = argv[4]


#---------------Starts Minimising Fucntion with Correct Mode---------------#
if mode == 'full':

    minimise(corpus_directory, parent_directory, full(target))
elif mode == 'sim':

    minimise(corpus_directory, parent_directory, sim(target))
elif mode == 'validate':

    minimise(corpus_directory, parent_directory, validate(target))
else:

    print('Invalid Bigrapher mode please select full, sim or validate.')
