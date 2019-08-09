#Creating a dictionary of phrase tags with it's corresponding heads according to the rules of the Hindi parser 
#to create chunks in English which are consistent with the chunks output by the Hindi parser.
import sys
from nltk.tree import ParentedTree
#eng=open('FormatForInputToEnglishHeadCode.txt',encoding='utf-8')
inp = sys.argv[1]
eng = open(inp, encoding = 'utf-8')
content = eng.read().split("\n")
#print(content)
allsent = []
allpos = []
   
list_of_phrase_tags=['VP','NP','ADJP','ADVP','PP']                #as in hindi parser
heads = {"NP":["NNS","NNP",'PRP','NN','NNPS'],               #corresponding heads for the phrases
             "VP":['VBP','VBZ','VBG','VBD','VBN','VB'],
             "ADJP":['JJR','JJS','JJ','VBN'],
             "ADVP":['RB','RBR'],
             "CC" : ['CC'],
             "PP" : ["IN"]
             }
check = ['RB','RBR','JJ','JJR','JJS']
counter = 0

# In[100]:


flag=True
for q in content:
    if q!= '' :
        counter += 1 
        q = q.replace(' (. .)','')
        print(counter)
        ptree = ParentedTree.fromstring(q)
        leaf_values = ptree.leaves()
        #print(ptree)
        #print(leaf_values)
        ##ptree.pretty_print()
        ls = []
        pos={}
        for x in ptree.leaves():
            i=-2
            leaf_index = leaf_values.index(x)
            tree_location = ptree.leaf_treeposition(leaf_index)
            y=str(ptree[tree_location[:i]])
            p=str(ptree[tree_location[:-1]])
            indexp = p.find(" ")
            indexnp = p.find("\n")
            if(indexnp<indexp and indexnp!=(-1)):
                indexp = indexnp
            pos.update({x:p[1:indexp]})
            while(i>-(ptree.height())):    # going up the parse tree till we dont get a chunk tag for the word as specifie by the list above
                indexy = y.find(" ")
                indexny = y.find("\n")
                if(indexny<indexy and indexny!=(-1)):
                    indexy = indexny
                if(y[1:indexy] in list_of_phrase_tags):
                    ls.append([x, y[1:indexy]])
                    break
                else:
                    i=i-1
                    y=str(ptree[tree_location[:i]])
        tag = ls[0][1]
        chunk=[]
        st = []
        i=0
        for x in ls:
            y = x[0]
            if(pos.get(y)=='CC'):
                if(flag):
                    chunk.append([tag,st])
                    st=[]
                st.append(y)
                tag="CC"
                chunk.append([tag,st])
                st = []
                flag=False
            elif (pos.get(y) in heads.get(x[1])):
                st.append(y)
                tag=x[1]
                chunk.append([tag,st])
                st =[]
                flag=False
            elif x[1]==tag:
                flag=True
                st.append(y)
            else:  
                if(flag):
                    chunk.append([tag,st])
                tag = x[1]
                st =[]
                st.append(y)
                flag=True
        if(len(st)>0):
            chunk.append([tag,st])
        newchunk = []
        for (i,x) in enumerate(chunk):
            if(i<len(chunk)-1):
                if i>0 and x[0]=='PP' and chunk[i+1][0]=='NP' and (chunk[i-1][0]=='NP' and pos.get(chunk[i-1][1][0]) in check):
                    chunk[i+1][1] = chunk[i-1][1] + x[1] + chunk[i+1][1]
                    newchunk.pop()
                    #newchunk.append(chunk[i+1])
                elif x[0]=='PP' and (chunk[i+1][0]=='NP' or chunk[i+1][0]=='VP') :
                    chunk[i+1][1] = x[1] + chunk[i+1][1]
                else:
                    newchunk.append(x)
            else:
                newchunk.append(x)
        for x in newchunk:
            for y in heads.keys():
                if x[0]==y:
                    l = heads.get(y)
                    for z in x[1]:
                        if pos.get(z) in l:
                            x[1].append(z)
                            break
        allsent.append(newchunk)
        allpos.append(pos)


# In[101]:


for x in allsent:
    for y in x:
        if len(y[1])==1:
            y[1].append(y[1][0])
            


# In[102]:


en = open('EnglishParsed.txt','w',encoding='utf-8')
for (j,i) in enumerate(allsent):
    en.write("SentenceID:" + str(j+1))
    en.write("\n")
    for x in i:
        en.write('*' + "\t" + x[0])
        en.write("\t")
        if(len(x[1])>0):
            en.write(x[1][-1])
            en.write("\n")
            for y in x[1][:len(x[1])-1]:
                en.write("@")
                en.write("\t")
                en.write(allpos[j].get(y))
                en.write("\t")
                en.write(y)
                en.write("\n")
    en.write("#")
    en.write("\n")
en.close()        
        


