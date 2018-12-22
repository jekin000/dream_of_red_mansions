#coding=utf-8

from pkuseg import pkuseg
import re
import pickle

def load_file(fname):
	with open(fname,'rb') as f:
		data = f.read()
	obj = pickle.loads(data)
	return obj

def parse_tuple(word):
	result = {}
	for i in range(0,len(word)-1):
		if (word[i]!='#' and word[i+1]!='#') and (len(word[i]) + len(word[i+1])>2):
			tup = (word[i],word[i+1])	
			num = result.get(tup,None)
			if num is None:
				result[tup] = 1
			else:
				result[tup] = num+1
	return result

def parse(seg,fname):
	f = open(fname,'r')
	data = f.readlines()
	all_text = []
	for each_para in data:		
		splited_segs = re.split(r'，|《|》|．|？|！|：|"|  |“|。|”', each_para.strip())
		for each_seg in splited_segs:
			if len(each_seg)>0:
				all_text.extend(seg.cut(each_seg))
			all_text.append('#')
		all_text.append('#')

	res = parse_tuple(all_text)
	twotuples = sorted(res.items(), key=lambda d: d[1])
	twotuples.reverse()
	return twotuples

def write_to_file(fname,data,src_fname):
	with open(fname,'a') as f:
		f.write('top 100 two-tuple  in {}:\n'.format(src_fname))
		f.write('No.\tTwo-Tuple\t\tCount\n')
		f.write('-----------------------------------\n')
		for i in range(0,100):
			if len(str(data[i][0])) < 12:
				f.write('{}\t{},\t\t{}\n'.format(i+1,str(data[i][0]),data[i][1]))
			else:
				f.write('{}\t{},\t{}\n'.format(i+1,str(data[i][0]),data[i][1]))
		f.write('\n')

def parse_and_write(seg,orifname,dstfname):
	data = parse(seg,orifname)
	write_to_file(dstfname,data,orifname)

if __name__ == '__main__':
	seg = pkuseg(user_dict=load_file('words'))
	parse_and_write(seg,'part1.txt','result.txt')
	parse_and_write(seg,'part2.txt','result.txt')
	parse_and_write(seg,'part3.txt','result.txt')

