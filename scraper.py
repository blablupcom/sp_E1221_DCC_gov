# -*- coding: utf-8 -*-

import scraperwiki
import urllib2
import urllib
import urlparse
from datetime import datetime
from bs4 import BeautifulSoup

# Set up variables
entity_id = "E1221_DCC_gov"
url = "https://www.dorsetforyou.com/article/400828"

# Set up functions
def convert_mth_strings ( mth_string ):
	month_numbers = {'JAN': '01', 'FEB': '02', 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09','OCT':'10','NOV':'11','DEC':'12' }
	#loop through the months in our dictionary
	for k, v in month_numbers.items():
		#then replace the word with the number
		mth_string = mth_string.replace(k, v)
	return mth_string

# pull down the content from the webpage
html = urllib2.urlopen(url)
soup = BeautifulSoup(html)
# find all entries with the required class
block = soup.find('div',{'id':'list'})
pageLinks = block.findAll('a', href=True)

for pageLink in pageLinks:
	pageUrl = 'https://www.dorsetforyou.com' + pageLink['href']
	if 'Dorset-County-Council---Expenditure-over-500---201' in pageUrl:
		parsed_link = urlparse.urlsplit(pageUrl.encode('utf8'))
		parsed_link = parsed_link._replace(path=urllib.quote(parsed_link.path))
		encoded_link = parsed_link.geturl()
	  	html2 = urllib2.urlopen(encoded_link)
		soup2 = BeautifulSoup(html2)
		fileLinks = soup2.findAll('a',href=True)
		for fileLink in fileLinks:
			url = 'http://www.dorsetforyou.com/' + fileLink['href']
			if '.csv' in url:
				#  clean up the onclick data
				title = fileLink.contents[0]
				title = title.encode('utf8').strip().replace("\n", " ").replace("\r", " ").replace("\t", " ")
				# create the right strings for the new filename
				csvYr = title.split(' ')[8]
				csvMth = title.split(' ')[7][:3]
				csvMth = csvMth.upper()
				csvMth = convert_mth_strings(csvMth);
				filename = entity_id + "_" + csvYr + "_" + csvMth + ".csv"
				todays_date = str(datetime.now())
				scraperwiki.sqlite.save(unique_keys=['l'], data={"l": url, "f": filename, "d": todays_date })
				print filename
