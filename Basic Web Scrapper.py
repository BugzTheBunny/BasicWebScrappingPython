#importing installed library
# @pandas
# @BeautifullSoap
from bs4 import BeautifulSoup
import requests
import pandas as db

#list
listOf_jobs={}
#job counter
job_no = 0
#This is the URL used for scraping
url = "https://boston.craigslist.org/search/npo"
while True:
	response = requests.get(url)
	data = response.text
	#Usin BS object for parsing, with html.parser (There are other options than html.parser)
	soup = BeautifulSoup(data,'html.parser')
	#searching for 'p' objects, with the name of 'result-info', and each result will be added to "jobs" collection
	jobs = soup.find_all('p',{"class":"result-info"})

	for job in jobs:

		#Basic Information
		#Searching for 'a' tags in the result
		title = job.find('a',{'class':'result-title'}).text
		location_tag = job.find('span',{'class':"result-hood"})
		location = location_tag.text[2:-1] if location_tag else 'UNKNOWN'
		date = job.find('time',{'class':'result-date'}).text
		link = job.find('a',{'class':'result-title'}).get('href')
		job_response = requests.get(link)
		job_data = job_response.text

		#Inner Pages information
		job_soup = BeautifulSoup(job_data, 'html.parser')
		job_description = job_soup.find('section',{'id':'postingbody'}).text	
		job_atri_tag = job_soup.find('p',{'class':'attrgroup'})
		job_atri = job_atri_tag.text if job_atri_tag else "NO INFO"

		#Jobs counter and dictionary updater
		job_no+=1
		listOf_jobs[job_no] = [title, location,date,link,job_atri,job_description]
		print('Job: ',job_no,' ', title, '\nLocation:' ,location, '\nDate: ',date,'\nLink: ',link,'\nJob Description: \n', job_description,'\nAtributes: ',job_atri,'\n------------------------------------')
		#Printing urls
	url_tag	= soup.find('a',{'title':'next page'})	
	if url_tag.get('href'):
		url = 'https://boston.craigslist.org' + url_tag.get('href')
		print(url)
	else:
		break
#printing the totals jobs that were found
print('Total Jobs: ', job_no)
#creating a frame (a stracture of information that is imported by pandas library, help data manipulation)
listOf_jobs_frame = db.DataFrame.from_dict(listOf_jobs, orient = 'index', columns = ['Job Title','Location','Date','Link','Attributes','Description'])
print(listOf_jobs_frame.head())
#exporting the information gotten into an csv file
listOf_jobs_frame.to_csv('theListOfJobs.csv')