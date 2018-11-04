import gearman
import sys
import urllib2
#import urllib.request as urlreq
from bs4 import BeautifulSoup as bs
import requests
from multiprocessing import Pool
import os
import getopt
import threading
import wikipedia
import sys
import codecs


from StringIO import StringIO 
gm_worker = gearman.GearmanWorker(['10.0.2.13:4730'])

def linklisting(search):
	linklist=[]
	url="http://www.google.com/search?"
	payload={'q':search}
	try:
		r=requests.get(url,payload,timeout=10)
		#print(r.url)
		print "--------------------------------".encode('utf-8')
		print "\t",search,"\t".encode('utf-8')
		print "--------------------------------".encode('utf-8')
#		print "1".encode('utf-8')
		if r.status_code ==200:
			html=r.text
			soup=bs(html,'lxml')
			weblist= soup.find_all('a')
			for link in weblist:
				a=link.get('href')
			
				if a.startswith("/url?q="):
					li=a[7:a.find('&sa')]
					if li not in linklist:
						linklist.append(li)
#						print "2".encode('utf-8')
	except Exception as ex:
		print(str(ex).encode('utf-8'))
	finally:
		return linklist
		
def parse(url):
	try:
#		print '3'.encode('utf-8')
		r=requests.get(url,timeout=10)
		
	
		
		if r.status_code==200:
			html=r.text
			soup=bs(html,'lxml')
			
			print soup.title.string.encode('utf-8'),' : '.encode('utf-8'),url.encode('utf-8'),'\n'.encode('utf-8')
			
	except Exception as ex:
		print str(ex).encode('utf-8')
		
def gsearch(search):
	linklist = []
	linklist=linklisting(search)
	#for i in linklist:
	#	print i.encode('utf-8')
	
	for i in linklist:
		parse(i)
		
def task_listener_gsearch(gearman_worker, gearman_job):
        old_stdout = sys.stdout 
        result = StringIO()
        print 'Job received for '+gearman_job.data.encode('utf-8')
        sys.stdout = result
 

        gsearch(gearman_job.data)

        sys.stdout = old_stdout
        print "Job completed for "+gearman_job.data.encode('utf-8')
        result_string=result.getvalue()

        result_string1=gearman_job.data

        return result_string


gm_worker.register_task('gsearch', task_listener_gsearch)


gm_worker.work()
