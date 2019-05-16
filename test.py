from __future__ import print_function
from bs4 import BeautifulSoup
import requests
import json
from collections import Counter

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


#Points system
point_per_run = 1
srate200 = 20
srate150 = 15
srate125 = 10
srate100 = 5
srate80 = 2
srate70=-5
sratelow=-10
minballsforsr=20
duck=-5
catch=10
stumping=15
runout=15
runs50=20
runs100=35
runs150=50
runs200=65
runs250=85
maiden=15
wicket = 25
rpo35=10
rpo45=5
rpo50=2
rpo60=0
rpo70=-2
rpo100=-5
rpohigh=-10
minoversforrr=3
wicket3=25
wicket4=40
wicket5=50
wicket6=60
wicket7=80
motmpoints=25

def main():
	f = open(r'D:\Reports and Data\CricketAutomation\AllGames.txt','rt')
	matches = []
	line = f.readline()
	while (line):
		matches.append(line)
		line = f.readline()
	f.close()
	i=0
	flag = True
	while(flag):
		link = matches[i].rstrip('\n').rstrip()
		page = requests.get(link)
		soup = BeautifulSoup(page.text, 'html.parser')
		motm = soup.find(class_="matchdetails")
		if motm is None:
			flag = False
		else:
			motm2 = motm.find_all("li")
			for t in motm2: 
				if ("PLAYER" in t.text):
					res=t.text.split(': ')[1].rstrip("\n").rstrip()
			if res == "TBD":
				pass
			else:
				CalcMatch(soup)
			i+=1
	f = open(r'D:\Reports and Data\CricketAutomation\AllGames.txt','wt')
	for x in range(i,len(matches)):
		f.write(matches[x])
	f.close()



def CalcMatch(soup):
	#page = requests.get(url)

	bat = soup.find_all(class_="tableview inningbat")
	team1 = Counter()
	team2 = Counter()
	artist_name_list_items = bat[0].find_all('td','')
	c=0
	for artist_name in artist_name_list_items:
		c+=1
		if('class' in artist_name.attrs and artist_name['class']!="middleinfo" and artist_name['class']!="hide1" ):
			pass
		else:
			if(c<78):
				t = artist_name.text.strip('\n')

				if(t.isdigit()):
					pass
				elif (t==''):
					pass
				else:
					tag = ""
					if '(' in t:
						tag = t.split(' (')[0]
					else:
						tag = t
					if len(tag)>3:
						try:
							team1[tag] += CalcBat(int(artist_name_list_items[c+1].text), int(artist_name_list_items[c+2].text), artist_name_list_items[c].text)
							s1,i1 =CalcField(artist_name_list_items[c].text)
							team2[s1] += i1
						except:
							team1[tag] += 0
						pass

	

	artist_name_list_items = bat[1].find_all('td','')
	c= 0 
	for artist_name in artist_name_list_items:
		c+=1
		if('class' in artist_name.attrs and artist_name['class']!="middleinfo" and artist_name['class']!="hide1" ):
			pass
		else:
			if(c<78):
				t = artist_name.text.strip('\n')
				if(t.isdigit()):
					pass
				elif (t==''):
					pass
				else:
					tag = ""
					if '(' in t:
						tag = t.split(' (')[0]
					else:
						tag = t
					if len(tag)>3:
						try:
							team2[tag] += CalcBat(int(artist_name_list_items[c+1].text), int(artist_name_list_items[c+2].text), artist_name_list_items[c].text)
							s1,i1 =CalcField(artist_name_list_items[c].text)
							team1[s1] += i1
						except:
							team2[tag] += 0
						pass
	
	bat = soup.find_all(class_="tableview inningbowl")
	artist_name_list_items = bat[0].find_all('td','')
	c=0
	while c< len(artist_name_list_items):
		artist_name = artist_name_list_items[c]
		c+=1
		if('class' in artist_name.attrs and artist_name['class']!="middleinfo" and artist_name['class']!="hide1" ):
			pass
		else:
			t=artist_name.text.strip("\n")
			score = CalcBowl(float(artist_name_list_items[c].text),int(artist_name_list_items[c+1].text),int(artist_name_list_items[c+3].text),float(artist_name_list_items[c+4].text))
			#print(artist_name.text)
			team2[t]+=score
			c+=6
			pass
	artist_name_list_items = bat[1].find_all('td','')
	c=0
	while c< len(artist_name_list_items):
		artist_name = artist_name_list_items[c]
		c+=1
		if('class' in artist_name.attrs and artist_name['class']!="middleinfo" and artist_name['class']!="hide1" ):
			pass
		else:
			t=artist_name.text.strip("\n")
			score = CalcBowl(float(artist_name_list_items[c].text),int(artist_name_list_items[c+1].text),int(artist_name_list_items[c+3].text),float(artist_name_list_items[c+4].text))
			#print(artist_name.text)
			team1[t]+=score
			c+=6
			pass
	try:
		motm = soup.find(class_="matchdetails")
		motm2 = motm.find_all("li")
		for t in motm2:
			if ("PLAYER" in t.text):
				res=t.text.split(': ')[1].rstrip("\n").rstrip()
		if res in team1:
			team1[res] += motmpoints
		else:
			team2[res] += motmpoints
	except:
		pass
	#j = json.dumps(soup.text)
	#print(json.dumps(j, indent=4, sort_keys=True))
	f3 = open(r'D:\Reports and Data\CricketAutomation\currentpoints.txt','wt')
	for key in team1:
		f3.write(key + '\t' + str(team1[key])+'\n')
	for key in team2:
		f3.write(key + '\t' + str(team2[key])+'\n')
	f3.close()
	TransformScores(team1,team2)
	PublishScores()

def CalcBat(i1, i2, s1):
	res = i1
	if (i1==0 and "not" not in s1):
		res+=duck #Add bowler criteria here
	if (i2 >= minballsforsr): 
		sr = i1 * 100 / i2
		if sr >= 200:
			res+=srate200
		elif sr>=150:
			res+=srate150
		elif sr>=125:
			res+=srate125
		elif sr>=100:
			res+=srate100
		elif sr>=80:
			res+=srate80
		elif sr>=70:
			res+=srate70
		else:
			res+=sratelow
	if(i1>=250):
		res+=runs250
	elif(i1>=200):
		res+=runs200
	elif(i1>=150):
		res+=runs150
	elif(i1>=100):
		res+=runs100
	elif(i1>=50):
		res+=runs50
	return res

def CalcField(string):
	if (string.startswith('c & b')):
		arr= string[6:].split(' ')
		
		res = arr[0][0]
		for a in range(1,len(arr)):
			res+=(" "+arr[a])
		return res, catch
	elif(string.startswith('c ') or string.startswith('st ')):
		s = string.split(' b ')[0]
		if string.startswith('c'):
			s = s[2:]
		else:
			s = s[3:]
		arr= s.split(' ')
		
		res = arr[0][0]
		for a in range(1,len(arr)):
			res+=(" "+arr[a])
		if string.startswith('c'):
			return res, catch
		else:
			return res, stumping
	elif(string.startswith('Run')):
		arr= string[8:].split(' ')
		
		res = arr[0][0]
		for a in range(1,len(arr)):
			res+=(" "+arr[a])
		return res, runout

def CalcBowl(i1,i2,i3,i4):
	res = 0
	res += i2*maiden
	res += i3*wicket
	if i1>minoversforrr:
		if i4<=3.5:
			res+=rpo35
		elif i4<=4.5:
			res+=rpo45
		elif i4<=5:
			res+=rpo50
		elif i4<=6:
			res+=rpo60
		elif i4<=7:
			res+=rpo70
		elif i4<10:
			res+=rpo100
		else:
			res+=rpohigh
	if i3>6:
		res+=wicket7
	elif i3>5:
		res+=wicket6
	elif i3>4:
		res+=wicket5
	elif i3>3:
		res+=wicket4
	elif i3>2:
		res+=wicket3
	return res

def TransformScores(c1, c2):
	CellDict={}
	TeamDict = {}
	col = ['D','E','F','G','H','I','J','K','L','M','N','O']
	Team = Counter()
	f1 = open(r'D:\Reports and Data\CricketAutomation\PlayerData.txt','rt')
	line = f1.readline()
	while(line):
		splitlines = line.split('\t')
		CellDict[splitlines[0]] = int(splitlines[1])
		TeamDict[splitlines[0]] = splitlines[2].rstrip('\n')
		line = f1.readline()
	f1.close()


	f2 = open(r'D:\Reports and Data\CricketAutomation\TeamGameInfo.txt','rt')
	line = f2.readline()

	while(line):
		splitlines = line.split('\t')
		Team[splitlines[0]]=int(splitlines[1])
		line = f2.readline()
	f2.close()
	team1 = TeamDict[c1.most_common()[0][0]]
	team2 = TeamDict[c2.most_common()[0][0]]
	team1col = col[Team[team1]]
	team2col = col[Team[team2]]
	Team[team1]+=1
	Team[team2]+=1
	f2 = open(r'D:\Reports and Data\CricketAutomation\TeamGameInfo.txt','wt')
	for t in Team:
		f2.write(t + "\t" + str(Team[t]) + "\n")
	f2.close()
	f1 = open(r"D:\Reports and Data\CricketAutomation\Points.txt","wt")
	for k in c1:
		try:
			f1.write(team1col+str(CellDict[k])+"\t"+str(c1[k])+"\n")
		
		except:
			pass
			
	for k in c2:
		try:
			f1.write(team2col+str(CellDict[k])+"\t"+str(c2[k])+"\n")
		except:
			pass		
	f1.close()

def PublishScores():
	SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

	SAMPLE_SPREADSHEET_ID = '1HLicKJymGiWY5ZgwxmXn_6y1Qe435lcDuPs3XdZYgyY'
	SAMPLE_RANGE_NAME = 'PointsAgg!A2:E4'

	creds = None


	with open(r'D:\Reports and Data\CricketAutomation\token.pickle', 'rb') as token:
		creds = pickle.load(token)
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				r'D:\Reports and Data\CricketAutomation\credentials.json', SCOPES)
			creds = flow.run_local_server()
		with open(r'D:\Reports and Data\CricketAutomation\token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	service = build('sheets', 'v4', credentials=creds)

	# Call the Sheets API
	sheet = service.spreadsheets()

	f = open(r'D:\Reports and Data\CricketAutomation\Points.txt','rt')
	line = f.readline()
	while (line):
		splitline = line.split('\t')
		ran = splitline[0]
		val = splitline[1].rstrip('\n')

		range_name = 'PointsAgg!'+ran
		values = [
		[val],
		]
		body = {
			'values': values
		}
		result = service.spreadsheets().values().update(
			spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_name,
			valueInputOption='USER_ENTERED', body=body).execute()
		line = f.readline()
	f.close()

	


if __name__ == '__main__':
	main()