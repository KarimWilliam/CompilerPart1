import argparse
import re
import os 

if __name__ == '__main__':
	parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

	parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?",
						metavar="file")

	args = parser.parse_args()

	print(args.file)


output_file =open("task_2_result.txt","w+")

# Open file
#file = open("args.file", 'r')

statecounter =0
statelist =[]
alphabetlist=[]
startstate ="q0"
finalstate="q0"
transitionlist=[]
worksbackwardslist=['*','+','?','|','.']
precedencelist=['(','|','.','?','*','+']
leftbrace,line,dot,question,star,plus=1,2,3,4,5,6
operatorlist=['*','?','+','|','.']

def opscore(op):
	if(op =="("):
		return 6
	elif(op =="|"):
		return 5
	elif (op =="."):
		return 4
	elif (op=="?"):
		return 3
	elif (op=="*"):
		return 2
	else:
		return 1


def fixconcatination(string):
	prev = '|'
	count=0
	newstring=''
	for c in string:
		if not (c in worksbackwardslist or c == ')' or prev == '|' or prev=='('):
			 newstring = newstring+'.'+c
		else:
			newstring = newstring + c
		count+=1
		prev=c
	print("newstring concatinated: "+newstring)
	return newstring

# (a*)  a   stack:(*
def ShuntingYardRegex(string):
	tempstack=[]
	poststack=[]
	newstring=''
	for c in string:
		if (c not in precedencelist and c!=")"):
			newstring=newstring+c
		elif (c=="("):
			poststack.append("(")
		elif (c==")"):
			while len(poststack)>0:
				if (poststack[-1]=="("): 
					poststack.pop()
					break
				else:
					newstring= newstring+poststack.pop()


		elif(  len(poststack)==0) or (poststack[-1]=="(" ):
			poststack.append(c)

			
		elif(c in operatorlist):
			if(opscore(c)>= opscore(poststack[-1])):
				poststack.append(c)
			else:
				for item in poststack:
					if(opscore(c)<= opscore(poststack[-1])):
						if(poststack[-1]=="("):
							poststack.pop()
						else:
							newstring=newstring+poststack.pop()
					else:
						poststack.append(c)
						break
	count =-1
	for item in poststack:
		newstring=newstring+poststack[count]
		count = count-1

	print("newstring: "+newstring)
	return newstring 


class node:
	def __init__(self, name, start, end):
		self.name = name
		self.start = start
		self.end = end





def concatinate(astart,aend,bstart,bend):
	global startstate
	global statecounter
	global finalstate
	global statelist
	global transitionlist
	global alphabetlist
	startstate="q"+str(astart)
	finalstate="q"+str(bend)

	for element in transitionlist:
		if(element[0]=="q"+str(bstart)):
			element[0]="q"+str(aend)
		
	for element in statelist:
		if(element =="q"+ str(bstart)):
			statelist.remove("q"+str(bstart))


	return(astart,bend)


def symbol(a):
	global statecounter
	global finalstate
	global statelist
	global transitionlist
	global alphabetlist

	statelist.append("q"+str(statecounter))
	statecounter+=1
	transition= ["q"+str((statecounter-1)),a,"q"+str(statecounter)]
	transitionlist.append(transition)
	alphabetlist.append(a)
	statelist.append("q"+str(statecounter))
	statecounter+=1

def union(astart,aend,bstart,bend):
	global startstate
	global statecounter
	global finalstate
	global statelist
	global transitionlist
	global alphabetlist
	alphabetlist.append(" ")
	startstate="q"+str(statecounter)

	transition= ["q"+str((statecounter)), " " ,"q"+str(astart)]  #q0 to q1
	transitionlist.append(transition)
	transition= ["q"+str((statecounter))," ","q"+str(bstart)]  #q0 to q3
	transitionlist.append(transition)

	start2=statecounter
	statelist.append("q"+str(statecounter))
	statecounter+=1


	transition= ["q"+str((aend))," ","q"+str(statecounter)]  #q2 to q5
	transitionlist.append(transition)

	transition= ["q"+str((bend))," ", "q"+str(statecounter)]  #q4 to q5
	transitionlist.append(transition)

	end2=statecounter
	finalstate="q"+str(statecounter)
	statelist.append("q"+str(statecounter))
	statecounter+=1

	return(start2,end2)


def kleene(start,end):
	global startstate
	global statecounter
	global finalstate
	global statelist
	global transitionlist
	global alphabetlist
	alphabetlist.append(" ")
	transition= ["q"+str((end))," ","q"+str(start)]  #inside kleene
	transitionlist.append(transition)

	transition= ["q"+str((statecounter)), " ","q"+str(start)]  #q0 to q1
	transitionlist.append(transition)
	startstate="q"+str(statecounter)


	start2=statecounter
	statelist.append("q"+str(statecounter))
	statecounter+=1

	transition= ["q"+str((end))," ","q"+str(statecounter)]  #q2 to q3
	transitionlist.append(transition)

	transition= ["q"+str((start2))," ","q"+str(statecounter)]  #q0 to q3
	transitionlist.append(transition)

	end2=statecounter
	finalstate="q"+str(statecounter)
	statelist.append("q"+str(statecounter))
	statecounter+=1

	return(start2,end2)

def plus(start,end):
	global startstate
	global statecounter
	global statelist
	global transitionlist
	global alphabetlist
	alphabetlist.append(" ")
	transition= ["q"+str((end)), " ","q"+str(start)]  #inside plus
	transitionlist.append(transition)

	transition= ["q"+str((statecounter)), " ","q"+str(start)]  #q0 to q1
	transitionlist.append(transition)


	start2=statecounter
	statelist.append("q"+str(statecounter))
	statecounter+=1

	transition= ["q"+str((end))," ", "q"+str(statecounter)]  #q2 to q3
	transitionlist.append(transition)

	end2=statecounter
	finalstate="q"+str(statecounter)
	statelist.append("q"+str(statecounter))
	statecounter+=1

	startstate="q"+str(start2)
	return(start2,end2)


def questionmark(start,end):
	global startstate
	global statecounter
	global finalstate
	global statelist
	global transitionlist
	global alphabetlist
	alphabetlist.append(" ")

	transition= ["q"+str((statecounter)), " ","q"+str(start)]  #q0 to q1
	transitionlist.append(transition)
	startstate="q"+str(statecounter)


	start2=statecounter
	statelist.append("q"+str(statecounter))
	statecounter+=1

	transition= ["q"+str((end)), " ","q"+str(statecounter)]  #q2 to q3
	transitionlist.append(transition)

	transition= ["q"+str((start2)), " ","q"+str(statecounter)]  #q0 to q3
	transitionlist.append(transition)

	end2=statecounter
	finalstate="q"+str(statecounter)
	statelist.append("q"+str(statecounter))
	statecounter+=1

	return(start2,end2)


singelsymbollist=['?','*','+']

def regextoNFA(string):
	global statecounter
	regexlist= list(string)
	nodelist=[]
	print(regexlist)

	for element in regexlist:
		if not (element in precedencelist):
			symbol(element)
			x= node("operand",statecounter-2,statecounter-1)
			nodelist.append(x)
		else:
			nodelist.append(element)

	while len(nodelist)>2: 
		counter=0
		for element in nodelist:				
			if (element in precedencelist):
				if(element in singelsymbollist):
					operand= nodelist.pop(counter-1)
					operator= nodelist.pop(counter-1)

					if(operator=="*"):
						start,end=kleene(operand.start,operand.end)  #START, END 
						nodelist.insert(counter-1,node("operand",start,end))
					elif(operator=="+"):
						start,end=plus(operand.start,operand.end)  #START, END 
						nodelist.insert(counter-1,node("operand",start,end))

					elif(operator=="?"):
						start,end=plus(operand.start,operand.end)  #START, END 
						nodelist.insert(counter-1,node("operand",start,end))

				else:
					operand1= nodelist.pop(counter-2)
					operand2= nodelist.pop(counter-2)
					operator= nodelist.pop(counter-2)

					if(operator=="."):
						start,end=concatinate(operand1.start,operand1.end,operand2.start,operand2.end)
						nodelist.insert(counter-2,node("operand",start,end))

					elif(operator=="|"):
						start,end=union(operand1.start,operand1.end,operand2.start,operand2.end)
						nodelist.insert(counter-2,node("operand",start,end))


				break
			counter+=1





#file = open(args.file, 'r')
regextoNFA(ShuntingYardRegex(fixconcatination("(0|(1(01*(00)*0)*1)*)*"))) #"(0|(1(01*(00)*0)*1)*)*"  file.read()

alphabetlist = list(set(alphabetlist)) #make alphabet unique elements
statelist = list(set(statelist)) #make list unique elements
print(statelist)
print(alphabetlist)
print(startstate)
print(finalstate)
print(transitionlist)
output_file.write(','.join(statelist)+'\n'+','.join(alphabetlist)+'\n'+startstate+'\n'+finalstate+'\n')
transitionlisttuple=[]

for x in transitionlist:
	transitionlisttuple.append( tuple(x))

for x in transitionlisttuple:
	output_file.write(str((x))+", ")

output_file.seek(-1, os.SEEK_END)
output_file.truncate()
output_file.seek(-1, os.SEEK_END)
output_file.truncate()


output_file.close()