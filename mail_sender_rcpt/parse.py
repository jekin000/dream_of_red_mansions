#coding=utf-8 

import re
def parse_mail_indexes(filename):
	with open(filename,'r') as f:
		contents = f.readlines()
	p = re.compile(r'From .*tomcat.apache.org@tomcat.apache.org.*')
	begin_indexs = []
	for i in range(0,len(contents)):
		res = p.search(contents[i])	
		if res is not None:
			begin_indexs.append(i)
	return begin_indexs,contents
		
def extract_owner(string):
	p = re.compile(r'<.*>')
	res = p.search(string)
	if res is None:
		return None
	s = re.sub('<.*>|\\\"|,|=[0-9]*','',string)
	s1 = re.sub('\\[.*?\\]','',s)
	s2 = re.sub(' +',' ',s1)
	s3 = s2.strip().replace(' ','_')
	return s3

def extract_subject(string):
	return string.strip()

def extract_date(string):
	return string.strip()

def parse_each_mail(contents):
	owner = ''
	subject = ''
	date = ''
	for line in contents:
		if 'From: ' in line:
			owner  = extract_owner(line.split(':')[1])
			if owner is None:
				return None,None,None
		elif 'Subject: ' in line:
			subject = extract_subject(line.split(':')[1])
		elif 'Date: ' in line:
			date = extract_date(line.split(':')[1])
	return owner,subject,date

def parse_email(indexes_array,contents):
	all_keyvalues = {}
	for i in range(0,len(indexes_array)-1):
		owner,subject,date = parse_each_mail(contents[indexes_array[i]+1:indexes_array[i+1]-1])
		if owner is None:
			continue
		key   = '_{}_{}{}'.format(owner,subject,date)
		value = '{}#{}#{}'.format(owner,subject,date)
	        all_keyvalues[key] = value	
	return all_keyvalues

import json
def write_json_data(filename,data):
	jsondata = json.dumps(data)
	with open(filename,'w') as f:
		f.write(jsondata)


if __name__ == '__main__':
	begin_indexes,contents = parse_mail_indexes('201201')
	all_keyvalues = parse_email(begin_indexes,contents) 
	write_json_data('from_keyvalue.txt',all_keyvalues)
