#!/usr/bin/python
import sys
import urllib.request as urlreq
from bs4 import BeautifulSoup as bs
import requests
from multiprocessing import Pool
import os
import getopt
import threading
import wikipedia


global word
global wlistpath
global printinfile
global wiki
global utilcount
wiki=False
utilcount =0

def usage():
	print("Syntax: python3 gcrawl [[-w WORD][-W WORDLIST][--words WORDS SEPERATED WITH ',']][--wiki]")
	print("Options:\n\t-w WORD or -W --wordlist WORDLIST\n\t--words for searching group of words individually separate the words with a comma ")
	exit()


def linklisting(search):
	linklist=[]
	url="http://www.google.com/search?"
	payload={'q':search}
	try:
		r=requests.get(url,payload,timeout=10)
		#print(r.url)
		print("--------------------------------")
		print("\t",search,"\t")
		print("--------------------------------")
		if r.status_code ==200:
			html=r.text
			soup=bs(html,'html.parser')
			weblist= soup.find_all('a') 
			for link in weblist:
				a=link.get('href')
			
				if a.startswith("/url?q="):
					li=a[7:a.find('&sa')]
					if li not in linklist:
						linklist.append(li)
	except Exception as ex:
		print(str(ex))
	finally:
		return linklist
		
def parse(url):
	try:
		r=requests.get(url,timeout=10)
	
	
		
		if r.status_code==200:
			html=r.text
			soup=bs(html,'lxml')
			
			print(soup.title.string,' : ',url,'\n')
			if (wiki== True and 'en.wikipedia' in url):
				search=url[30:]
				spcl_chars=['!','@','$','%','^','&','*','(',')','_','-','+','=']
				search1=""
				for i in search:
					if i in spcl_chars:
						search1+=" "
					else:
						search1+=i
				print("[*]Wikipedia Page Found: ",search1)
				u=wikipedia.summary(title=search1,sentences=5)
				print(u)
				print()
	
	except Exception as ex:
		print(str(ex))
			
def gsearch(search):
	html= None
	linklist = []
	linklist=linklisting(search)
	#for i in linklist:
	#	print(i)
	with Pool(5) as p:
		p.map(parse,linklist)
		p.terminate()
		p.join()
		

	
#main----------
if __name__=='__main__':

	print("****Web crawler/scraper(Google Terminal Client)****")

	try:
		opts, args=getopt.getopt(sys.argv[1:],("wW:h"),["wiki","help","wordlist=","words"])
		
	except getopt.GetoptError as err:
		print(err)
		usage()
	
		
	print("Number of arguements  :",len(sys.argv[1:]))	
	print("opts  :",opts)
	print("args  :",args)
	
	if len(sys.argv[1:])==0:
		usage()
	if "--wiki" in args:
			wiki=True
			utilcount+=1
	
	for i in range(0,utilcount):
		args.pop()
	print("args :",args);
	
	for o,a in opts:
		if o in ("-h","--help"):
			usage()
		
		elif o in ("-w"):
			search=""
			for i in args:
				search+=i+" "
			gsearch(search)				
			
		elif o in ("-W","--wordlist"):
			print("Searchlisting....\n")
			wlistpath=a
			print("Path of the Searchlist: ",wlistpath)
			wordlist=[]
			f=open(wlistpath , 'r')
			while f.mode=='r':
				strg=f.readline().strip()
				if strg=='':
					break
				wordlist.append(strg)
						
			else:
				print("File cannot be opened")
				exit()
						
			#for i in wordlist:
			#	t=threading.Thread(target=gsearch, args=(i,))
			#	t.start()
			
			for i in wordlist:
				gsearch(i)
		elif o in ("--words"):
			print("Individual searching for a bunch of words")
			s=""
			wlist=[]
			c=0
			a=args
			a.append(',')
			for i in a:
				if i==',':
					c+=1
			j=0
			for i in a:
				
				if (i==","):
					wlist.append(s)
					s=""
					j+=1
				else:
					s+=i+" "
					if j==c and s!='':
						wlist.append(s)
			print(wlist)
			#make search as a cache output and then rearrange them to display the results
			
			
			
			for i in wlist:
				gsearch(i)
		
		else:
			assert False,"Unhandled Option"
	




	

	



