from flask import Flask, render_template
import requests
import json
import os
import cgi, cgitb


app = Flask(__name__)
#using flask in order to work python script directly with html
@app.route('/')
def hello_world():
	#Here we return an html script and flask will interpret it as such instead of just string
	return '''
	<h1 align = center>Instant Intellectual!</h1>
<p align= center> Upload your work below and let us make it instantly sound 20x smarter!</p>

<form action="/fileUploaded" enctype =" multipart/form-data" method = "post">
  <input type="file" name="filename" accept=".txt*">
  <input type="submit" value="upload">

</form>
<a href="/fileUploaded">link</a>

<h2>That was a 200 IQ move but...what about a 400 IQ move ?!?!?!
<p align= left> Do another upload with the previous output to acheieve the maximum level of enlightenment!</p>

<img src = "{{url_for('static', filename='Galaxybrain.png')}}" title="Pretend Galaxy Brain Picture Here" height=350 width=450 />

<h3>Enjoy this masterpiece</h3>
	'''# + '<p>' + + '</p>' 
	
@app.route('/fileUploaded')
def test():
	#This is where we can output our result to the webpage by appending what our main() returns with html code
	return '''
		<h1 align = center>Here's your Output!<h1>
	''' + main()

def getLongest(strArr):
	#find the longest synonym for a word in the merriam webster thesaurus
	longest = ""
	for str in strArr:
		temp = str
		if len(temp) > len(longest):
			longest = temp
	return longest

def romanNum(num):
	#changes decimal number between 0 - 3999 to a roman numeral
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

def convertLine(strs, output, dic1, puncs):
	#changes line from original to big brained and returns new line
	#replaces word with its longest synonym and replaces numbers with roman numerals
	retStr = ""
	prev_period = True
	punc = False
	temp = ''

	for s in strs:
		if s == "I" or s == 'i': 
			retStr += "I "
			continue
		if s[0].isupper() and prev_period == False:
			retStr += s
			retStr += " "
			continue
		if s[0] in dic1.keys() or s[0] == '-' and s[1] in dic1.keys():
			if s[len(s)-1] in puncs:
				temp = s[len(s)-1]
				punc = True
				s = s[:-1]
			if s[0] == '-':
				s = romanNum(s[1:])
				s = '-' + s
			else:
				s = romanNum(s)
		else:
			periodCheck = False
			if s[len(s)-1] == '.' :
				periodCheck = True
				s = s[:-1] 
			elif s[len(s)-1] in puncs:
				temp = s[len(s)-1]
				output.write(temp)
				punc = True
				s = s[:-1]
			try:
				#use api key to access merriam webster thesaurus api which varies by string and comes as a json file
				response = requests.get("https://dictionaryapi.com/api/v3/references/" + "thesaurus" "/json/" + s + "?key=6b5adf9a-ae9b-4da9-bbd1-48c0e06c7541")
				bigj = response.json()
				syn = getLongest(bigj[0]['meta']['syns'][0])
				if bigj[0]['fl'] == 'noun' or bigj[0]['fl'] == 'adjective' and (len(syn) > len(s)):
					s = syn
			except:
				#case where the string s is not in the dictionary(Proper Nouns, weird words)
				retStr += s + " "
				prev_period = False
				if s[len(s)-1] in ",?!":
					prev_period = True
				continue
		if not prev_period and not punc:
			retStr += s
			retStr += " "
		elif prev_period:
			retStr += s.capitalize()
			retStr += " "
			prev_period = False
		elif punc:
			output.write("here")
			retStr += s
			retStr += temp
			if temp == '!' or temp == '?':
				prev_period = True

			retStr += " "
			punc = False
		else:
			retStr += s.capitalize()
			retStr += " "
			prev_period = False

		if periodCheck :
			retStr += ".  "
			prev_period = True
		else:
			retStr += " " 
	return retStr

def main():
	# cgitb.enable()
	# form = cgi.FieldStorage()
	# #str = input("File to generate: ")
	# file = form['upload']
	# if file.filename:
	# 	fn = os.path.basename(fileitem.filename)
	# 	open('/tmp/' + fn, 'r')
	# 	print("File: " + fn + "uploaded successfully")
	file = open('t3.txt', 'r')
	lines = file.readlines()
	file.close()
	out = open('output.txt', 'w')
	num_dic = {}
	punc_array = ",;:!?"
	#create dictionary to check if a string is a number in convertLine function
	for i in range(0, 10):
		num_dic[str(i)] = 0
	ret_string = ""
	for line in lines:
		strs = line.split()
		ret_string += convertLine(strs, out, num_dic, punc_array)
	return ret_string
	out.close()

main()