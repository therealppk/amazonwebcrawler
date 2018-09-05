from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import matplotlib.pyplot as plt
dict={}
    
def extract_asin(r):
    
    a = requests.get(r)
    soup = BeautifulSoup(a.text, 'html.parser')
    a=str(a.text)
    mydivs = soup.findAll("li", {"class": "s-result-item"})
    count=0
    ans_author=list()
    ans_title=list()
    ans_asin=list()
    ans_price=list()

    for i in range(len(mydivs)):
        if count>=10:
            break
        soupi=BeautifulSoup(str(mydivs[i]), 'html.parser')
        mystarcheck=soupi.find("i",{"class":"a-icon-star"})
        if not mystarcheck:
            continue
        mytitle=soupi.find("h2",{"class":"s-access-title"})
        myauthor=soupi.findAll("div",{"class":"a-spacing-none"})
        soupij=BeautifulSoup(str(myauthor[2]), 'html.parser')
        myauthor=soupij.find("a",{"class":"a-text-normal"})
        if not myauthor:
            myauthor=soupij.findAll("span",{"class":"a-size-small"})
            myauthor=myauthor[1]
        
        myprice=soupi.findAll("span",{"class":"s-price"})
        f=[float(s) for s in re.findall(r'-?\d+\.?\d*', str(myprice))]
        #print('Count: ',count)
        #print('Product: ',mytitle['data-attribute'])
        #print('ASIN: ',mydivs[i]['data-asin'])
        #print('Author: ',myauthor.string)
        #print("Price: ",f[0])
        #print("\n")
        ans_asin.append(mydivs[i]['data-asin'])
        ans_author.append(myauthor.string)
        ans_price.append(f[0])
        ans_title.append(mytitle['data-attribute'])
        dict.update({'title':ans_title})
        dict.update({'author':ans_author})
        dict.update({'asin':ans_asin})
        dict.update({'price':ans_price})
        count+=1
ASIN=[]


print('Enter URL')
r=input()
extract_asin(r)
#print(df)
df=pd.DataFrame(data=dict)
df=df.sort_values('price')
writer = pd.ExcelWriter('output.xlsx',engine='xlsxwriter')
df.to_excel(writer,'Sheet1')
writer.save()
df.to_csv('file_name.csv', sep='\t')
print(df)
x=df[['price']].values
x=list(map(list, zip(*x)))[0]
y=[1,2,3,4,5,6,7,8,9,10]
plt.bar(y,x)
tis=df[['title']].values
tis=list(map(list, zip(*tis)))[0]
plt.xticks(y,tis,rotation=70)
print(x,y)
plt.show()
