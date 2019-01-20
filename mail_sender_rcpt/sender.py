import json

#calc sendcnt for each owner
def generate_send_count(data):
	sendcnts = {}
	for key in data.keys():
		value = data.get(key)
		name = value.split('#')[0] 
		if sendcnts.has_key(name):
			sendcnts[name] = sendcnts[name]+1
		else:
			sendcnts[name] = 1
	return sendcnts

#dump the senders data to disk
def make_data():
	content = ''
	with open('from_keyvalue.txt','r') as f:	
		content = f.read()

	formated = json.loads(content)
	senders = generate_send_count(formated)
	with open('senders.txt','w') as f:
		f.write(json.dumps(senders))

	return senders

def make_debug_data():
	senders = make_data()
	output = ['{} {}\n'.format(key,senders[key]) for key in sorted(senders.keys())]

	with open('debug_senders.txt','w') as f:
		f.writelines(output)

import os
def clean():
	try:
		os.remove('senders.txt')
		os.remove('debug_senders.txt')
	except OSError as e:
		pass

if __name__ == '__main__':
	make_debug_data()
