lines = open('kats_rech.txt', encoding='utf8').readlines()
i = 0
current_str = ''
for line in open('kats_rech.txt', encoding='utf8').readlines():
	if ':' in line: continue
	i += 1
	current_str += line.lower().replace('\n', '') + ' '
	if len(current_str) > 130:
		print(current_str)
		current_str = ''

print(current_str)
