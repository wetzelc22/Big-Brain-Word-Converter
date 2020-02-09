import requests
import json
import os
import cgi, cgitb

def getLongest(strArr):
	longest = ""
	for str in strArr:
		temp = str
		#print(str + "length of this string is = \n")
		#print(len(str))
		if len(temp) > len(longest):
			longest = temp
	return longest

def romanNum(num):
	num = int(num)
	nums = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
	romans = ['M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I']
	romanNum = ''
	i = 0
	while num >= 0:
		#print(num)
		#print(nums[i])
		if nums[i] <= num:
			romanNum += romans[i]
			num -= nums[i]
		else:
			i+=1
		if(i == 13):
			break

	return romanNum

#def romanNum(strNum):
	#check for punc

def convertLine(strs, output, dic1, puncs):
	#loaded = json.loads(text)
	#for x in loaded:
	#need to account for punctuation
	prev_period = True
	punc = False
	temp = ''
	for s in strs:
		if s == "I" or s == 'i': 
			output.write("I ")
			continue
		if s[1].isupper():
			output.write(s)
			continue
		if s[0] in dic1.keys() or s[0] == '-' and s[1] in dic1.keys():
			if s[0] == '-':
				s = romanNum(s[1:])
				s = '-' + s
			#s = romanNum(s)
			#check for period in there
		else:
			periodCheck = False
			if s[len(s)-1] == '.' :
				periodCheck = True
				s = s[:-1] 
			elif s[len(s)-1] in puncs:
				temp = s[len(s)-1]
				punc = True
				s = s[len(s)-1]
			response = requests.get("https://dictionaryapi.com/api/v3/references/" + "thesaurus" "/json/" + s + "?key=6b5adf9a-ae9b-4da9-bbd1-48c0e06c7541")
			bigj = response.json()
			syn = getLongest(bigj[0]['meta']['syns'][0])
			if bigj[0]['fl'] == 'noun' or bigj[0]['fl'] == 'adjective' and (len(syn) > len(s)):
				s = syn
		#now have individual string
		if not prev_period:
			output.write(s)
		elif punc:
			output.write(s)
			output.write(punc)
			output.write(" ")
		else:
			output.write(s.capitalize())
			prev_period = False

		if periodCheck :
			output.write(".  ")
			prev_period = True
		else:
			output.write(" ")

def main():
	cgitb.engable()
	form = cgi.FieldStorage()
	#str = input("File to generate: ")
	file = form['upload']
	if file.filename:
		fn = os.path.basename(fileitem.filename)
		open('/tmp/' + fn, 'r')
		print("File: " + fn + "uploaded successfully")
	else:
		print("fuck")

	#file = open('t.txt', 'r')
	lines = file.readlines()
	file.close()
	out = open('output.txt', 'w')
	num_dic = {}
	punc_array = ",;:!?"
	for i in range(0, 10):
		num_dic[str(i)] = 0
	for line in lines:
		strs = line.split()
		convertLine(strs, out, num_dic)

main()