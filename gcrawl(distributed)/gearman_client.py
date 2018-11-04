import gearman
import getopt
import sys
def check_request_status(job_request):
    if job_request.complete:
        print "Job %s finished!  Result: %s - %s" % (job_request.job.unique, job_request.state, job_request.result)
    elif job_request.timed_out:
    #time_out=30 secs
        print "Job %s timed out!" % job_request.unique
    
def usage():
	print "****Web crawler/scraper(Google Terminal Client)****"
	print "For Example:\n\tpython gearman_client.py -W a.txt"
	exit()



wordlist=[]
try:
	opts, args=getopt.getopt(sys.argv[1:],("W:h"),["help","wordlist="])
		
except getopt.GetoptError as err:
	print(err)
	usage()

if len(sys.argv[1:])==0:
		usage()
		
for o,a in opts:
	if o in ("-h","--help"):
			usage()
	elif o in ("-W","--wordlist"):
			print "****Web crawler/scraper(Google Terminal Client)****"
			print("Starting search....\n")
			wlistpath=a
			print "Path of the Searchlist: ",wlistpath
			
			f=open(wlistpath , 'r')
			while f.mode=='r':
				strg=f.readline().strip()
				if strg=='':
					break
				wordlist.append(strg)
						
			else:
				print("File cannot be opened")
				exit()
						
			
#wordlist=["Hello world","Taylor Swift","Viktor"]

gm_client = gearman.GearmanClient(['localhost:4730'])
#gm_client1 = gearman.GearmanClient(['10.0.2.17:4730'])


new_jobs=[dict(task='gsearch', data=i) for i in wordlist]

#for i in range(0,len(wordlist)):
	#completed_job_request = gm_client.submit_job("gsearch", wordlist[i],wait_until_complete=True)
	#check_request_status(completed_job_request)
	#completed_job_request1 = gm_client1.submit_job("gsearch", wordlist[i+1],wait_until_complete=True)
	#check_request_status(completed_job_request1)
	


completed_requests = gm_client.submit_multiple_jobs(new_jobs)
for current_request in completed_requests:
    
    check_request_status(current_request)
    
