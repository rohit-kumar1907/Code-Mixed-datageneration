#eng=open('FormatForInputToEnglishHeadCode.txt',encoding='utf-8')
#content = eng.read().split("\n")
#for q in content:
    	
eng = open('IITBombayEng.txt', encoding= 'utf-8')
hin = open('IITBombayHin.txt', encoding= 'utf-8')
content_eng = eng.read().splitlines()
content_hin = hin.read().splitlines()
#print(content)
list1= []
list2= []
counter1 = 0
counter2 = 0
dis= open('discard_sent.txt','w',encoding='utf-8')
en = open('clean_eng.txt', 'w', encoding='utf-8')
hi = open('clean_hin.txt', 'w', encoding='utf-8')        
 
for q1, q2 in zip(content_eng, content_hin):
    if q1!='' and q2!='':
        counter1+=1
        counter2+=1
        if '. .' in q1:
            #dis=open('discard_sent.txt','a',encoding='utf-8')
            dis.write(str(counter1)+"\n")
            dis.write(q1+"\n")
            dis.write(q2+"\n")
            #dis.close()
           # print (counter1)
        else:
            #en = open('clean_eng.txt', 'a', encoding='utf-8')
            #hi = open('clean_hin.txt', 'a', encoding='utf-8')
            en.write(q1+"\n")
            hi.write(q2+"\n")
            #en.close()
            #hi.close()
print('Done')
        
