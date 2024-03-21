"""
This file scans all bib, tex and cls files to try and find characters that latex won't like.
It is not foolproof, sadly.
"""

import sys
import os
import os.path, fnmatch, time
import subprocess
import argparse 
import re 
import chardet
import shutil

def listFiles(root, patterns='*.bib;*.cls;*.tex', recurse=1, return_folders=0, useRegex=False):
    """Lists the files/directories meeting specific requirement

        Returns a list of file paths to files in a file system, searching a 
        directory structure along the specified path, looking for files 
        that matches the glob pattern. If specified, the search will continue 
        into sub-directories.  A list of matching names is returned. The 
        function supports a local or network reachable filesystem, but not URLs.

    Args:
        | root (string): directory root from where the search must take place
        | patterns (string): glob/regex pattern for filename matching. Multiple pattens 
          may be present, each one separated by ;
        | recurse (unt): flag to indicate if subdirectories must also be searched (optional)
        | return_folders (int): flag to indicate if folder names must also be returned (optional)
        | useRegex (bool): flag to indicate if patterns areregular expression strings (optional)

    Returns:
        | A list with matching file/directory names

    Raises:
        | No exception is raised.
    """
    if useRegex:
        import re

    # Expand patterns from semicolon-separated string to list
    pattern_list = patterns.split(';')
    filenames = []
    filertn = []

    for dirpath,dirnames,files in os.walk(root):
        if dirpath==root or recurse:
            for filen in files:
                # filenames.append(os.path.abspath(os.path.join(os.getcwd(),dirpath,filen)))
                filenames.append(os.path.relpath(os.path.join(dirpath,filen)))
            if return_folders:
                for dirn in dirnames:
                    # filenames.append(os.path.abspath(os.path.join(os.getcwd(),dirpath,dirn)))
                    filenames.append(os.path.relpath(os.path.join(dirpath,dirn)))

    for name in filenames:
        if return_folders or os.path.isfile(name):
            for pattern in pattern_list:
                if useRegex:
                    #search returns None is pattern not found
                    regex = re.compile(pattern)
                    if regex.search(name):
                        filertn.append(name)
                        break
                else:
                    # split only the filename to compare, discard folder path
                    if fnmatch.fnmatch(os.path.basename(name), pattern):
                        filertn.append(name)
                        break
    return filertn

#####################################################################################
def getFileEncoding(filename):
    """Determine and return the file encoding""" 
    from chardet.universaldetector import UniversalDetector
    detector = UniversalDetector()
    detector.reset()
    for line in open(filename, 'rb'):
        detector.feed(line)
        if detector.done: break
    detector.close()
    return detector.result['encoding']

#####################################################################################
def CheckFileContents(filename):

    print(f'Processing {filename}')
    
   # these are the only acceptable chars allowed in our input
    # acceptable = set(chr(i) for i in range(0x0, 0xFF + 1))
    acceptable = set(chr(i) for i in range(0x0, 0x7F))

    # print(f'file {filename} uses {chardet.detect(filename)}')
    encoding = getFileEncoding(filename)
    # print(f'{encoding}  {type(encoding)} file {filename}')

    if encoding is None or 'ascii' not in encoding:
            print(f'file {filename} uses encoding "{encoding}"')
            with open(filename,'r', encoding='utf-8') as fin:
                lines = fin.readlines()
                bad_strings = filter(lambda s:  not set(s).issubset(acceptable), lines)
                print(filename)
                for blitem in list(bad_strings):
                    print(blitem,end='\n')     
    else:
        pass
    fin  = open(filename, encoding=encoding )
    lines = fin.readlines()
    fin.close()
    linecnt=0
    for line in lines:
        linecnt = linecnt+1
        try:
            position = line.find(r"\begin{document}")
        except: # catch all errors
            print('Problem with character with code >128 in file {0}, line {1}\n'.format(filename, linecnt))
        if position > -1:     
            break  
    return

#####################################################################################
def CheckFileName(filename):


    
   # these are the only acceptable chars allowed in our input
    # acceptable = set(chr(i) for i in range(0x0, 0xFF + 1))
    acceptable = set(chr(i) for i in range(0x0, 0x7F))
    bad_strings = filter(lambda s:  not set(s).issubset(acceptable), filename)
    if len(list(bad_strings))>0:
        print(f'{filename}') 
        print(list(bad_strings))

 
    return

#####################################################################################

filenames = listFiles('.')

for filename in filenames:
    # print(filename)    
    CheckFileName(filename)
    # CheckFileContents(filename)
