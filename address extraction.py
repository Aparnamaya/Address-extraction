#Spazer tool for processing web pages
#

from bs4 import BeautifulSoup
import pathlib
import re


#Variables to track the input, output and gained space
space_gained = 0
space_input = 0
space_output = 0

print("Welcome to Spazer\n")

for x in range(10):
    filename = str(x) + ".html"
    file = pathlib.Path('input/' + filename)
    if (file.exists()):

        #Reading each file
        print("Reading " + filename)
        f = open('input/' + filename, 'r', errors="ignore")
        contents = f.read()   
        check1=re.compile(r".*(address|Address|ADDRESS).*")
        check2=re.compile(r"\b\d\d\d(\s)*\d\d\d\b")
        check3=re.compile(r"(.*(e-mail).*(^(\+91-|\+91|0)?[6789]\d{9}$))|(.*(email).*(^(\+91-|\+91|0)?[6789]\d{9}$))|(.*(e-mail).*(^(\+91-|\+91|0)?[6789]\d{9}$))")
        #Removing html tags
        soup=BeautifulSoup(contents,'html.parser')
        addrs=soup.find_all("address")
        out=""
        for i in addrs:
            out=out+i.get_text()
        classes=soup.find_all(class_=check1)
        for i in classes:
            out=out+i.get_text()
        ids=soup.find_all(id=check1)
        for i in ids:
            out=out+i.get_text()
        out1 = soup.find_all(re.compile(r".*"), string=check1)
        temp1=""
        for i in out1:
            temp1=temp1+i.parent.get_text()
        for i in re.finditer(check1,temp1):
            out=out+(temp1[(i.start()):(i.start()+200)]).strip()
        out2 = soup.find_all(re.compile(r".*"), string=check2)
        temp2=""
        for i in out2:
            temp2=temp2+i.parent.get_text()
        for i in re.finditer(check2,temp2):
            r=(temp2[(i.start()-200):(i.start()+10)]).strip()
            if r not in out:
                out=out+r
        out3 = soup.find_all(re.compile(r".*"), string=check3)
        temp3=""
        for i in out3:
            temp3=temp3+i.parent.get_text()
        for i in re.finditer(check3,temp3):
            r=(temp2[(i.start()-200):(i.start()+10)]).strip()
            if r not in out:
                out=out+r
        #Writing the output variable contents to output/ folder.
        print ("Writing reduced " + filename)
        fw = open('output/' + filename, "w")
        fw.write(out)
        fw.close()
        f.close()
        
        #Calculating space savings
        space_input = space_input + len(contents)
        space_output = space_output + len(out)
 
        
space_gained = round((space_input - space_output) * 100 / space_input, 2)

print("\nTotal Space used by input files = " + str(space_input) + " characters.") 
print("Total Space used by output files = " + str(space_output) + " characters.")
print("Total Space Gained = " + str(space_gained) + "%") 
       
    











