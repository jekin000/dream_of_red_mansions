import json

def generte_subjects(sender_data):
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

#TODO
def sorted_by_date(tuple_list):
	return ''

#TODO
def generate_rcpt(sorted_tuple_list):
	return ''
	
if __name__ == '__main__':
	content = ''
	with open('from_keyvalue.txt','r') as f:	
		content = f.read()

	formated = json.loads(content)
	subjects = generte_subjects(formated)
	for key in  subjects.keys():
		print subjects[key]

	for each_subject in subjects.keys():
		subjects[each_subject] = sorted_by_date(subjects[each_subject])

	
	for each_subject in subjects.keys():
		subjects[each_subject] = generate_rcpt(subjects[each_subject])

	with open('rcpts.txt','w') as f:	
		f.write(json.dumps(subjects))

