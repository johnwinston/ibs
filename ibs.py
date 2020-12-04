from subprocess import PIPE, Popen
from datetime import datetime
import random
import golly as g
import re

out = []
err = []
patDepth = 1
maxDepth = 0
width = 0
pat = ""

# Configure
partPath = "PATH_TO_PARTIAL_OUTPUT_FOLDER"
gollyPath = "PATH_TO_GOLLY_FOLDER"
ikpx2Path = "PATH_TO_IKPX2_EXECUTABLE"
velocity = "IKPX2_COMPATIBLE_VELOCITY"
patName = datetime.utcnow()
minValidRows = 5 #[0, x]
threads = 8
key = "CATAGOLUE_KEY"
decisionWidth = 10
maxWidth = 15


while True:
    cmd = ikpx2Path + " -v \'" + velocity + "\' -p 1 " + gollyPath + "/Scripts/Python/pat.rle"
    depth = 0
    while True:
        g.randfill(25)
        if 0 != int(g.getpop()):
            break
    g.update()
    g.save("pat.rle", "rle")
    process = Popen(
                [cmd],
                shell=True,
                stdout=PIPE,
                stderr=PIPE
                )
    i = 0
    fullBreak = False
    while True:
        err.append(process.stderr.readline().decode("ascii"))
        if 'valid rows:' in err[i]:
            print(err[i])
            if 'valid rows: [0,' in err[i]:
                digits = re.findall(r'\b\d+\b', err[i])
                patDepth = int(digits[3])
                if (patDepth < minValidRows):
                    fullBreak = True
                break
            fullBreak = True
            break
        i += 1

    process.terminate()
    del err[:]
    del out[:]
    if fullBreak:
        continue

    cmd = ikpx2Path + " -v \'" + velocity + "\' -p " + str(threads) + " -m " + str(patDepth) + " -k " + key + " " + gollyPath + "/Scripts/Python/pat.rle"
    process = Popen(
                [cmd],
                shell=True,
                stdout=PIPE,
                stderr=PIPE
                )
    i = 0
    found = True
    while True:
        out.append(process.stdout.readline().decode("ascii"))
        print(out[i])
        if 'depth = ' in out[i]:
            digits = re.findall(r'\b\d+\b', out[i])
            depth = int(digits[0])
            if (depth > maxDepth):
                maxDepth = depth
                found = False
                pat += out[i]
        elif 'width ' in out[i]:
            digits = re.findall(r'\b\d+\b', out[i])
            width = int(digits[0])
            if (width >= decisionWidth):
                if (depth <= 0):
                    del err[:]
                    del out[:]
                    break
                if (width >= maxWidth):
                    del err[:]
                    del out[:]
                    patName = datetime.utcnow()
                    maxDepth = 0
                    break
        elif (found == False):
            if '!' in out[i]:
                found = True
                pat += out[i]
                f = open(partPath+str(patName)+".rle", "w")
                f.write(pat)
                f.close()
                pat = ""
            else:
                pat += out[i]
        i += 1
    
    process.terminate()
