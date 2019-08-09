#Opening files
eng = open('EnglishParsed_0.txt',encoding='utf-8')
content = eng.read().split("\n")
hin = open('HindiParsed_0.txt',encoding='utf-8')
content1 = hin.read().split("\n")
eng.close()
hin.close()
content.pop()
content1.pop()


# For extracting information from the parsed files and storing all of them in lists
phrases_hin = []
phrase_tags_hin = []
heads_hin=[]
pos_tags_hin=[]
temp_pos = ""
temp_phrase=""
temp_all_tags=[]#store all the tags  of corresponding heads a sentence
temp_all_heads=[]#Store all the heads of a sentence
temp_all_pos=[]# Stores all the Pos tags of the phrases
temp_all_phrases=[]# Stores all the phrases of a sentences with their heads and corresponding tails.




for i in content1:
    if i[0]=='#':
        temp_all_phrases.append(temp_phrase)
        phrases_hin.append(temp_all_phrases)
        temp_all_pos.append(temp_pos)
        pos_tags_hin.append(temp_all_pos)
        heads_hin.append(temp_all_heads)
        phrase_tags_hin.append(temp_all_tags)
        temp_all_phrases=[]
        temp_all_pos=[]
        temp_phrase=""
        temp_pos = ""
        temp_all_tags=[]
        temp_all_heads=[]
    if i[0]=='*':
        tag=i.split("\t")[1]
        head=i.split("\t")[2]
        if(len(temp_phrase)):
            temp_all_phrases.append(temp_phrase)
            temp_all_pos.append(temp_pos)
        temp_phrase=""
        temp_pos=""
        temp_all_tags.append(tag)
        temp_all_heads.append(head)
    if i[0]=='@':
        temp_phrase = temp_phrase + (i.split("\t")[2]) + " "
        temp_pos = temp_pos + (i.split("\t")[1]) + " "
        
        


phrases_eng = []
phrase_tags_eng = []
heads_eng=[]
temp_all_phrases=[]# Stores all the phrases of a sentences with their heads and corresponding tails.
temp_phrase=""
temp_all_tags=[]#store all the tags  of corresponding heads a sentence
temp_all_heads=[]#Store all the heads of a sentence


for i in content:
    if i[0]=='#':
        temp_all_phrases.append(temp_phrase)
        phrases_eng.append(temp_all_phrases)
        heads_eng.append(temp_all_heads)
        phrase_tags_eng.append(temp_all_tags)
        temp_all_phrases=[]
        temp_phrase=""
        temp_all_tags=[]
        temp_all_heads=[]
    if i[0]=='*':
        tag=i.split("\t")[1]
        head=i.split("\t")[2]
        if(len(temp_phrase)):
            temp_all_phrases.append(temp_phrase)
        temp_phrase=""
        temp_all_tags.append(tag)
        temp_all_heads.append(head)
    if i[0]=='@':
        temp_phrase = temp_phrase + (i.split("\t")[2]) + " "
        


#Replacing maximum 3 NPs in english sentence with corresponding hindi NP
#Can change the count to how many ever sentences that you need to replace
newsentenceseng = []
temp_sent = []
replacement_phrase = []

#Gets a list of all possible translations for the english word input in decreasing order of probabilities
def get_list_from_file(eng_word): 
    feng=open('NiceSortEng.txt',encoding='utf-8')
    fhin=open('NiceSortHin.txt',encoding='utf-8')
    line_eng=feng.read().split('\n')
    line_hin=fhin.read().split('\n')

    feng.close()
    fhin.close()

    match=[]
    i=0
    for i in range(len(line_eng)):
        tokens=line_eng[i].split(' ')
        if(tokens[0]==eng_word):
            match.append(tokens[1])
    for i in range(len(line_hin)):
        tokens=line_hin[i].split(' ')
        if(tokens[0]==eng_word):
            match.append(tokens[1])

    return match


# Replacing NPs
flag = False
dem_flag = False
psp_flag = False
rp_flag = False
count = 0
for (i,x) in enumerate(phrase_tags_eng):
    count=0
    for (j,y) in enumerate(x):
        if y=='NP' and count<3:
            if(psp_flag or rp_flag):
                temp_sent.append(replacement_phrase)
                psp_flag=False
                rp_flag=False
            flag=False
            dem_flag=False
            head = heads_eng[i][j]
            matches = get_list_from_file(head)
            for (c,z) in enumerate(heads_hin[i]):
                if z in matches:
                    replacement_phrase=phrases_hin[i][c]
                    allpos = list(pos_tags_hin[i][c].split(" "))
                    if 'DEM' in allpos:
                        dem_flag=True
                        break
                    if allpos[len(allpos)-2] in ['PSP','RP']:
                        psp_flag = True
                        rp_flag = True
                        flag=True
                        new_replacement = ' '.join(replacement_phrase.split(' ')[:-2])
                        break
                    count = count + 1
                    flag=True
                    break
            if(flag!=True):
                temp_sent.append(phrases_eng[i][j])
            elif(psp_flag==False and rp_flag==False):
                temp_sent.append(replacement_phrase)
            
        else:
            if((psp_flag or rp_flag)):
                if(y=='VP'):
                    temp_sent.append(new_replacement)
                else:
                    temp_sent.append(replacement_phrase)
                psp_flag=False
                rp_flag = False
            temp_sent.append(phrases_eng[i][j])
    if(psp_flag or rp_flag):
        temp_sent.append(replacement_phrase)
        psp_flag=False
        rp_flag = False
    newsentenceseng.append(temp_sent)
    temp_sent = []
counter =0
#Writing into a file    
codemixed = open("CodeMixedEnglish_0.txt",'w',encoding='utf-8')
for i in newsentenceseng:
    counter+=1
    print(counter)
    codemixed.write(" ".join(x for x in i))
    codemixed.write("\n")
codemixed.close()
