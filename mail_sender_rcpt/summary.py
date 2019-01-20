
import json

import parse as parsemodule
import sender as sendermodule
import rcpt as rcptmodule
def make_data():
	parsemodule.make_data()
	sendermodule.make_data()
	rcptmodule.make_data()

	subject_rcpts_str = ''
	with open('rcpts.txt','r') as f:
		subject_rcpts_str = f.read()	
	subject_rcpts = json.loads(subject_rcpts_str) 

	senders_str = ''
	with open('senders.txt','r') as f:
		senders_str = f.read()	
	senders = json.loads(senders_str)

	rcpts = [subject_rcpts[key] for key in subject_rcpts.keys()]

	#init summary's sender data
	summary = {}
	for owner in senders.keys():
		summary[owner] = {'sendcnt':senders[owner],'rcptcnt':0}

	#update summary's rcpt data
	for rcpt in rcpts:
		name_cnt = rcpt.split(' ')
		name = name_cnt[0]
		rcptcnt = int(name_cnt[1].split('#')[0])
	
		if summary.has_key(name):
			summary[name]['rcptcnt'] = summary[name]['rcptcnt'] + rcptcnt 
		else:
		        summary[name] = {'sendcnt':senders[name],'rcptcnt':rcptcnt}	

	output_lines = sorted(['{} {} {}\n'.format(each_owner
			,summary[each_owner]['sendcnt']
			,summary[each_owner]['rcptcnt'])  for each_owner in summary.keys()])
		
	with open('summary.txt','w') as f:
		f.writelines(output_lines)

def clean_temp_data():
	parsemodule.clean()
	sendermodule.clean()
	rcptmodule.clean()

if __name__ == '__main__':
	make_data()
	clean_temp_data()
