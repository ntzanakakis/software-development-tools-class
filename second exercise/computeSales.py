import re
import os.path
import decimal
IDs= {}
flag=True
while flag:
    choice = input("Give your preference:\n1: read new input file\n2: print statistics for a specific product\n3: print statistics for a specific AFM\n4: exit the program\nInput: ")
    if choice=='1':
        file_name=input("Give file name:")
        if not(os.path.isfile(file_name)):
            continue
        file=open(file_name, encoding='utf-8')
        file_lines=file.readlines()  #read all file_lines and save on list
        count = len(file_lines)
        receipt_total=0
        c=0
        receipt_start = []
        no_space = []
        fields = []
        prod_fields=[]
        for i in range(0, count):
            if (re.search("^[-]+$", file_lines[i].rstrip())):
                receipt_start.append(i)             
        for i in range(0,len(receipt_start)-1):
            flag2=False
            no_space.clear()
            fields.clear()
            prod_fields.clear()
            receipt_total=0
            if not(re.search("ΑΦΜ: [0-9]{10}$", file_lines[(receipt_start[i]+1)].rstrip())): #true if line ISN'T in the format "AFM: 0123456789"
                continue
            
            for e in range (0,(receipt_start[i+1]-2) - (receipt_start[i]+1) ):
                no_space.append(" ".join(file_lines[(receipt_start[i]+e+2)].split()))
                prod_fields=no_space[e].split(":") #splits string into fields me a colon delimiter
                fields=(prod_fields[1].strip()).split(" ") #splits string into fields with space delimiter
                receipt_total += float(fields[2]) #holds food total
                if decimal.Decimal(fields[0])*decimal.Decimal(fields[1])!=decimal.Decimal(fields[2]): #if quantity*price!=total of food
                    flag2=True
                    break
            if flag2  :
                continue
            no_space.clear()
            total_line=(file_lines[(receipt_start[i+1]-1)].rstrip()).split(" ")#splits total line at the space'
            if not(re.search("ΣΥΝΟΛΟ: [0-9]+.[0-9]{2}$", file_lines[(receipt_start[i+1]-1)].strip())): #true if line ISN'T in the format "SYNOLO: 0123.01"
                continue
            elif float(total_line[1])!= float("{0:.2f}".format(receipt_total)): #true if food total != receipt total
                continue
                
            afm= (file_lines[(receipt_start[i]+1)].rstrip()).split(" ")
            if IDs.get(afm[1])==None:
                IDs[(afm[1])]={}
            for b in range (0,(receipt_start[i+1]-2) - (receipt_start[i]+1) ):
                no_space.append(" ".join(file_lines[(receipt_start[i]+b+2)].split()))
                prod_fields=no_space[b].split(":")
                fields=(prod_fields[1].strip()).split(" ") #splits string into fields with space delimiter
                prod_fields[0]= prod_fields[0].upper()
                if (IDs[(afm[1])].get(prod_fields[0])):                 
                    IDs[(afm[1])][(prod_fields[0])] += float(fields[2])
                else:
                    IDs[(afm[1])][(prod_fields[0])] = float(fields[2])
            no_space.clear()
            prod_fields.clear()
        file.close()
    if choice=='2':
        prod_in = input("Give product name: ")
        prod = (prod_in).upper()
        for afm in (sorted(IDs)):
            if prod in (IDs[afm]):
                print (afm, "%.2f" % round(IDs[afm][prod],2))
    if choice=='3':
        afm = input("Give AFM: ")
        if afm in IDs:
            for elem in sorted((IDs[afm]).items()):
                print ((elem[0])," ","%.2f" % round(elem[1],2))
    if choice=='4':
            print("Exiting...")
            flag=False
