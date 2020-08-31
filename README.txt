Cmin

This script can be split into 2 functions, first it calls afl-cmin on any given cropus directory and removes files that repeat behaviour. It then splits the minimised corpus into smaller directories, spins up new terminal windows and starts tmin processes on the new terminals. The script will call each bigrapher mode sequntially (full mode -> sim mode -> validate mode) unless a mode is specified when the script is called in which case the sciprt will run 1 mode only.

Tmin

This script will move through every file in a directory and call afl-tmin which will minimise a file to the smallest number of bits that still create new behaviours. This script will then copy all files back to the corpus directory that cmin created.

General notes

The scripts attempted to isolate bigrapher specific code to isolated methods where possible. The code can be re-purposed by editing the methods used to call cmin or tmin with application specific syntax and editing of the parsing section at the bottom of each script.

Parrelisation was achived through the creation of terminal instances due to the way the AFL works. AFL calls 1 process per terminal so if traditional methods of parrallel processing are used such as python.Pool, AFL will run synchronus processing not asynchronus. But by creating new terminals and calling processes on each terminal, afl can be run asynchronusly.