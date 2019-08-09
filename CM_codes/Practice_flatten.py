# Python script to flatten the constituent parsed tree structure into single sentence
import sys
inp = sys.argv[1]
inpFD = open(inp, 'r', encoding ='utf-8')
lines = inpFD.readlines()
for line in lines :
   if line != '\n' :
      line = line.replace('  ','')
      line = line.strip('\n')
      tempFD = open('c1_'+inp, 'a', encoding='utf-8')
      tempFD.write(line)
      tempFD.close()
   else :
      tempFD = open('c1_'+inp, 'a', encoding='utf-8')
      tempFD.write(line)
      tempFD.close()
      
