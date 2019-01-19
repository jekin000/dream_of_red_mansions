#coding=utf-8 


import re
def parse_mail_indexes(filename):
	fp = open(filename,'r')
	contents = fp.readlines()
	fp.close()

	p = re.compile(r'From .*tomcat.apache.org@tomcat.apache.org.*')
	begin_indexs = []
	for i in range(0,len(contents)):
		res = p.search(contents[i])	
		if res is not None:
			begin_indexs.append(i)
	return begin_indexs,contents
		
		

if __name__ == '__main__':
	begin_indexes,contents = parse_mail_indexes('201201')
	for i in range(0,len(begin_indexes)-1):
		print begin_indexes[i],begin_indexes[i+1]
