
# Song titles and duration in screen dump image.  
# Song title first and the duration on the right-hand side. in min:sec format as follows:
# this could be the title  4:34

# use tesseract to OCR the image with titles and song duration
# tesseract test.png --psm 4 test
# you may have to do some editing on the this text file

# Now process the text file created by tesseract to get into audacity label format
# then import as labels.
# http://manual.audacityteam.org/man/importing_and_exporting_labels.html

# the first column has the start time in seconds, the second column has the end time, 
# and the third column if present shows the text of the label. 
# Start time and end time are identical for a point label. 
# Values are separated by tab characters 
# for a point label:
# <label start> <tab> <label start> <tab> <title>

with open('test.txt','r') as fin:
    lines = fin.readlines()

with open('aud.txt','w') as fout:
    nextsong = 0
    track = 1
    for line in lines:
        if len(line) > 2:
            line = line.strip()
            # these are not allowed in filenames: * ? \ / : " < > |
            line = line.replace('>',' ')
            line = line.replace('<',' ')
            line = line.replace('|','I')
            line = line.replace('"',' ')
            line = line.replace(':','')
            line = line.replace('/',' ')
            line = line.replace('.',' ')
            line = line.replace('?',' ')
            line = line.replace('\\',' ')

            llst = line.split()
            title = ' '.join(llst[:-1])
            print('{}  >{}< >{}<  >{}<'.format(track,title,llst[-1][:-2],llst[-1][-2:]))
            songsecs = int(llst[-1][:-2]) * 60 + int(llst[-1][-2:])
            # create a point lable with zero duration
            newline = '{}\t{}\t{:02d}  {}'.format(nextsong,nextsong,track,title)
            # print(newline)
            fout.write('{}\n'.format(newline))
            nextsong += songsecs + 0.5
            track += 1

    