# Imports
import requests
import os
import sys

# For debugging, set to True.
verbose = False

def download_file(url, filename):
    local_filename = filename

    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)
    return local_filename

def extract_string(html, startingIndex, endingCharacter):
	string = ''
	while html[startingIndex] != endingCharacter:
		string = string + html[startingIndex]
		startingIndex = startingIndex + 1
	return string

username = sys.argv[1]
password = sys.argv[2]
quality = sys.argv[3]

# String constants
loginUrl = 'http://gdcvault.com/api/login.php'
logoutUrl = 'http://gdcvault.com/logout'

# Input Validation
if username == "":
	print("username is missing.")
	quit()

if password == "":
	print("password is missing.")
	quit()

if quality != 'low' and quality != 'high':
	print("quality: *" + quality + "* is invalid. Please select low or high.")
	quit()

# Read all urls from videoURLS.txt
urlList = []
f = open('videoURLS.txt', 'r')
for line in f:
	urlList.append(line)

# Login
response = requests.post(loginUrl, data={'email': username, 'password': password})
print('Login status code: ' + str(response.status_code))
if response.status_code == 500:
	print("500 returned on login. Aborting.")
	quit()

# Set cookies
phpsession = response.cookies['PHPSESSID']
userHash = response.cookies['user_hash']
cookies = dict(PHPSESSID=phpsession,
			   user_hash=userHash)

# In case shit happens
try:

	# Loop over all videos
	for url in urlList:

		videoUrl = url
		print('videoUrl: ' + videoUrl)

		# Load video page
		response = requests.get(videoUrl, cookies=cookies)
		print('Video page status code: ' + str(response.status_code))
		pageHtml = response.text

		# Extract xml id index
		startingIndex     = pageHtml.find('http://evt.dispeak.com/ubm/gdc/sf17/playerv.html?xml=') + 53
		if startingIndex == 52:
			startingIndex = pageHtml.find('http://evt.dispeak.com/ubm/gdc/sf17/player.html?xml=') + 52

		xmlId = extract_string(pageHtml, startingIndex, '.')

		if verbose:
			print('XML ID: ' + xmlId)	

		# Load video XML file
		# Example
		# http://evt.dispeak.com/ubm/gdc/sf17/xml/846788_JSAJ.xml
		response = requests.get('http://evt.dispeak.com/ubm/gdc/sf17/xml/' + xmlId + '.xml')
		print('XML file status code: ' + str(response.status_code))
		pageHtml = response.text

		startingIndex = pageHtml.find('assets/ubm/gdc/sf17/' + xmlId) + len('assets/ubm/gdc/sf17/' + xmlId) + 1
		secretCode = extract_string(pageHtml, startingIndex, '-')
		print('secretCode: ' + secretCode)	

		# Select video quality
		videoQuality = ''
		if quality == 'low':
			videoQuality = '500'
		elif quality == 'high':
			videoQuality = '1300'

		# Building actual video source url
		srcUrl = 'http://s3-2u-d.digitallyspeaking.com/assets/ubm/gdc/sf17/' + xmlId + '-' + secretCode + '-' + videoQuality + '.mp4'
		print('srcUrl: ' + srcUrl)

		startingIndex = pageHtml.find('<title><![CDATA[') + len('<title><![CDATA[')
		filename = extract_string(pageHtml, startingIndex, ']')

		# Remove invalid windows filename characters
		filename = filename.replace('<', '')
		filename = filename.replace('>', '')
		filename = filename.replace(':', '-')
		filename = filename.replace('"', '')
		filename = filename.replace('/', '')
		filename = filename.replace('\\', '')
		filename = filename.replace('|', '-')
		filename = filename.replace('?', '')
		filename = filename.replace('*', '')
		filename = filename + '.mp4'

		# Download file
		localFileName = download_file(srcUrl, filename)
		print("localFileName: " + localFileName)

		# Move video file to videos directory
		os.rename(localFileName, "videos/" + localFileName)

except Exception as inst:
	print('Exception!')
	print(type(inst))
	print(inst.args)
	print(inst)
	
	# Logout
	response = requests.get(logoutUrl, cookies=cookies)
	print('Logout status code: ' + str(response.status_code))

# Logout
response = requests.get(logoutUrl, cookies=cookies)
print('Logout status code: ' + str(response.status_code))
