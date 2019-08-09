from wxconv import WXC
import sys
inp = sys.argv[1]
hindi = open(inp)
con = WXC(order='wx2utf', lang='hin')
content = hindi.read().split("\n")
temp_phrase_sent = []
temp_tags_sent = []
temp_pos_sent = []
temp_heads = []
temp_phrase = ""
temp_pos = ""
phrases_all = []
phrase_tags_all = []
pos_tags_all = []
heads_all = []
#print(con.convert(hin))#Here hin is having having hindi text as multiple input

counter =0
count=0
for i in content:
    if len(i)>0:
        counter = counter + 1
        if i.split("\t")[0]=='</Sentence>':
            count = count+1
            phrases_all.append(temp_phrase_sent)
            phrase_tags_all.append(temp_tags_sent)
            pos_tags_all.append(temp_pos_sent)
            heads_all.append(temp_heads)
            temp_phrase_sent = []
            temp_pos_sent = []
            temp_tags_sent = []
            temp_heads = []
        elif i[1] =='.' or i[2]=='.':
            temp_phrase = temp_phrase + " " + i.split("\t")[1]
            temp_pos = temp_pos + " " + i.split("\t")[2]
           # print(i.split("\t")[1])
        elif i.split("\t")[1]=='))':
            print(counter)
            if len(temp_phrase)>0:
                temp_phrase_sent.append(temp_phrase)
                temp_pos_sent.append(temp_pos)
                temp_phrase = ""
                temp_pos = ""
        elif i.split("\t")[1]=='((':
            temp_tags_sent.append(i.split('\t')[2])
            to_find_head = i.split('\t')[3]
            x = list(to_find_head.split(" "))
#Here we're searching for the head and then converting it to UTF from WX
            for y in x:
                if len(y)>4:
                    if y[0:4]=='head':
                        head=y[6:len(y)-2]
            temp_heads.append(con.convert(head))            
            
            
            
            
en = open('HindiParsed_'+inp,'w',encoding='utf-8')
for (j,i) in enumerate(phrases_all):
    en.write("SentenceID:" + str(j+1))
    en.write("\n")
    for (c,x) in enumerate(i):
        en.write('*' + "\t" + phrase_tags_all[j][c])
        en.write("\t")
        en.write(con.convert(heads_all[j][c]))
        en.write("\n")
        words = list(x.split(" "))
        pos = list(pos_tags_all[j][c].split(" "))
        for (d,y) in enumerate(words[1:]):
            en.write("@")
            en.write("\t")
            en.write(pos[d+1])
            en.write("\t")
            en.write(y)
            en.write("\n")
    en.write("#")
    en.write("\n")
en.close()        
        
