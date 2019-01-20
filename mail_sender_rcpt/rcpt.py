import json

# generate the datas which key is subject
# name#subject#date -->   subject:(date,name)
def generate_subjects(sender_data):
	subjects = {}
	for each_key in sender_data:
		raw_list = sender_data[each_key].split('#')
		name = raw_list[0]
		subject = raw_list[1]
		date = raw_list[2]
		if subjects.has_key(subject):
			subjects[subject].append((date,name))
		else:
			subjects[subject] = [(date,name)]
		
	return subjects

from datetime import datetime,timedelta
import re

# transfer the date to struct which we could compare them.
def transfer_date(timestr):
	if '(UTC)' in timestr:
		timestr = re.sub('\(UTC\)','',timestr)		
	pos = timestr.find('+')	
	if pos == -1:	
		pos = timestr.find('-')	
	if pos == -1:
		return datetime.strptime(timestr,'%a, %d %b %Y %H:%M:%S  %Z')

	#before +/- HHMM
	ret = datetime.strptime(timestr[0:pos-1],'%a, %d %b %Y %H:%M:%S')
	if timestr[pos]=='+':
		ret-=timedelta(hours=int(timestr[pos+1:pos+3]),minutes=int(timestr[pos+3:]))
	elif timestr[pos]=='-':
		ret+=timedelta(hours=int(timestr[pos+1:pos+3]),minutes=int(timestr[pos+3:]))
	return ret

def sorted_by_date(tuple_list):
	newtuples = []
	for t in tuple_list:
		newtuples.append((transfer_date(t[0]),t[1]))
	return sorted(newtuples,key=lambda item:item[0])

#The earliest people will be the owner of this subject
#calc the data for this owner
def generate_rcpt(sorted_tuple_list):
	owner = sorted_tuple_list[0][1]
	if len(sorted_tuple_list) == 1:
		return '{} 0#0'.format(owner)

	replycnt = 0
	owncnt = 0
	for i in range(1,len(sorted_tuple_list)):
		if sorted_tuple_list[i][1] == owner:
			owncnt = owncnt+1	
		else:
			replycnt = replycnt+1
	return '{} {}#{}'.format(owner,replycnt,owncnt)


def make_data():
	content = ''
	with open('from_keyvalue.txt','r') as f:	
		content = f.read()

	formated = json.loads(content)
	subjects = generate_subjects(formated)

	for each_subject in subjects.keys():
		subjects[each_subject] = sorted_by_date(subjects[each_subject])

	
	for each_subject in subjects.keys():
		subjects[each_subject] = generate_rcpt(subjects[each_subject])

	with open('rcpts.txt','w') as f:	
		f.write(json.dumps(subjects))

	return subjects


def make_debug_data():
	subjects = make_data() 
	output = sorted(['{}  {}\n'.format(subjects[key],key) for key in subjects.keys()])
	with open('debug_rcpts.txt','w') as f:
		f.writelines(output)
import os
def clean():
	try:
		os.remove('debug_rcpts.txt')
		os.remove('rcpts.txt')
	except OSError as e:
		pass

if __name__ == '__main__':
	make_debug_data()
