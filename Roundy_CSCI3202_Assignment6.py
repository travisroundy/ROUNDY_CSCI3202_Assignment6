import getopt, sys

class Node():
	#---------------------------------------
	#Initializes the Node Class:
	#---------------------------------------
	def __init__(self):
		self.value = float
		self.condProb = []
		self.parent = []
		self.children = []
		self.letter = str

def setPrior(node, newValue):
	#------------------------------------------------
	#Updates the prior value to the new value given:
	#------------------------------------------------
	node.value = newValue
	newValue = str(newValue)
	print ("Prior Value Updated to: " + newValue)
	
	
def calcMarginal(a, node):
	#-------------------------------------------------------------------
	#Depening on the input, it will calculate the marginal probability,
	#including the negated form (~):
	#-------------------------------------------------------------------
	print a,node.letter
	originalNode = node
	if node.letter == "P":
		if (a == "~P") or (a == "~p"):
			print (1-node.value)
		else:
			print (node.value)
		
	elif node.letter == "S":
		if (a == "~S") or (a == "~s"):
			print (1-node.value)
		else:
			print (node.value)
		
	elif node.letter == "C":
		Poll = node.parent[0]
		Smoke = node.parent[1]
		highPnotS = 0.02 * (1-Smoke.value) * (1-Poll.value)
		highPyesS = 0.05 * Smoke.value * (1-Poll.value)
		lowPnotS = 0.001 * (1-Smoke.value) * (Poll.value)
		lowPyesS = 0.03 * Smoke.value * Poll.value
		margProb = (highPnotS + highPyesS + lowPnotS + lowPyesS)
		node.value = margProb
		if (a == "~C") or (a == "~c"):
			print ("-m~C = ", (1-margProb))
		else:
			print ("-mC = ", margProb)
		
	elif node.letter == "X":
		Cancer = node.parent[0]
		Poll = Cancer.parent[0]
		Smoke = Cancer.parent[1]
		PC1 = 0.02 * (1-Smoke.value) * (1-Poll.value)
		PC2 = 0.05 * Smoke.value * (1-Poll.value)
		PC3 = 0.001 * (1-Smoke.value) * (Poll.value)
		PC4 = 0.03 * Smoke.value * Poll.value
		PC = PC1 + PC2 + PC3 + PC4
		PX = 0.9 * PC + 0.2 * (1-PC)
		originalNode.value = PX
		if (a == "~X") or (a == "~x"):
			print ("-m~X = ", (1-PX))
		else:
			print ("-mX = ", PX)
		
	elif node.letter == "D":
		Cancer = node.parent[0]
		Poll = Cancer.parent[0]
		Smoke = Cancer.parent[1]
		PC1 = 0.02 * (1-Smoke.value) * (1-Poll.value)
		PC2 = 0.05 * Smoke.value * (1-Poll.value)
		PC3 = 0.001 * (1-Smoke.value) * (Poll.value)
		PC4 = 0.03 * Smoke.value * Poll.value
		PC = PC1 + PC2 + PC3 + PC4
		PD = 0.65 * PC + 0.3 * (1-PC)
		originalNode.value = PD
		if (a == "~D") or (a == "~d"):
			print ("-m~D = ", (1-PD))
		else:
			print ("-mD = ", PD)
	
def calcConditional(arg1, arg2, nodeList):
	#-------------------------------------------------------------------
	#Depening on the input, this calculates the conditional probability,
	#this has the values from the table for Predictive and Intercausal
	#-------------------------------------------------------------------
	print arg1,arg2,nodeList
	LowHigh = "Low"
	PosNeg = "Pos"
	node1 = nodeList[0]
	node2 = nodeList[1]
	node1Val = node1.value
	node2Val = node1.value
	if "~" in arg1:
		node1Val = (1-node1.value)
		if "p" in arg1:
			LowHigh = "High"
		elif "x" in arg1:
			PosNeg = "Neg"
	if "~" in arg2:
		node2Val = (1-node2.value)
		if "p" in arg2:
			LowHigh = "High"
		elif "x" in arg2:
			PosNeg = "Neg"
	if node1.letter == "C":
		if node2.letter == "S":
			Poll = node1.parent[0]
			PCS = 0.05 * node2.value * (1-Poll.value)
			PCS = PCS + 0.03 * node2.value * (Poll.value)
			PCS = PCS / node2.value
			print "-g'c|s' = ",PCS
		elif node2.letter == "P":
			Smoke = node1.parent[1]
			PCP = 0.05 * node2.value * (Smoke.value)
			PCP = PCP + 0.02 * node2.value * (1-Smoke.value)
			PCP = PCP / node2.value
			print "-g'c|p' = ",PCP
		elif node2.letter == "D":
			Poll = node1.parent[0]
			Smoke = node1.parent[1]
			calcMarginal(arg1,node1)
			PDC = 0.65 * 0.05
			PDC = PDC + 0.65 * 0.02
			PDC = PDC + 0.3 * 0.95 
			PDC = PDC + 0.3 * 0.98 
			denom = 0.05 
			denom = denom + 0.02 
			denom = denom + 0.95 
			denom = denom + 0.98 
			PDC = PDC / denom
			PCD = (PDC * (node1.value)) / (node1.value)
			print "-g'c|d' = ",PCD
			
	elif node1.letter == "P":
		if node2.letter == "S":
			print "-g'p|s' = ",(1-node1.value)
		elif node2.letter == "C":
			calcMarginal(arg2,node2)
			PC = node2.value
			Smoke = node2.parent[1]
			PCP = 0.05 * node2.value * (Smoke.value)
			PCP = PCP + 0.02 * node2.value * (1-Smoke.value)
			PCP = PCP / node2.value
			PPC = (PCP * (1-node1.value)) / PC
			print "-g'p|c' = ",PPC
		elif node2.letter == "D":
			Cancer = node1.children[0]
			Smoke = Cancer.parent[1]
			calcMarginal(arg2,node2)
			PDP = 0.65 * 0.05 * (1-node1.value) * (Smoke.value)
			PDP = PDP + 0.65 * 0.02 * (1-node1.value) * (1-Smoke.value)
			PDP = PDP + 0.3 * 0.95 * (1-node1.value) * (Smoke.value)
			PDP = PDP + 0.3 * 0.98 * (1-node1.value) * (1-Smoke.value)
			denom = 0.05 * (1-node1.value) * (Smoke.value)
			denom = denom + 0.02 * (1-node1.value) * (1-Smoke.value)
			denom = denom + 0.95 * (1-node1.value) * (Smoke.value)
			denom = denom + 0.98 * (1-node1.value) * (1-Smoke.value)
			PDP = PDP / denom
			PPD = (PDP * (1-node1.value)) / (node2.value)
			print "-g'p|d' = ",PPD
			
	elif node1.letter == "S":
		if node2.letter == "S":
			print "-g's|s' = ",(node2.value / node2.value)
		elif node2.letter == "C":
			calcMarginal(arg2,node2)
			PC = node2.value
			Poll = node2.parent[0]
			PCS = 0.05 * node1.value * (1-Poll.value)
			PCS = PCS + 0.03 * node1.value * (Poll.value)
			PCS = PCS / node1.value
			PSC = (PCS * node1.value)/PC
			print "-g's|c' = ",PSC
		elif node2.letter == "D":
			Cancer = node1.children[0]
			Poll = Cancer.parent[0]
			calcMarginal(arg2,node2)
			PDS = 0.65 * 0.05 * (node1.value) * (1-Poll.value)
			PDS = PDS + 0.65 * 0.03 * (node1.value) * (Poll.value)
			PDS = PDS + 0.3 * 0.95 * (node1.value) * (1-Poll.value)
			PDS = PDS + 0.3 * 0.97 * (node1.value) * (Poll.value)
			denom = 0.05 * (node1.value) * (1-Poll.value)
			denom = denom + 0.03 * (node1.value) * (Poll.value)
			denom = denom + 0.95 * (node1.value) * (1-Poll.value)
			denom = denom + 0.97 * (node1.value) * (Poll.value)
			PDS = PDS / denom
			PSD = (PDS * (node1.value)) / (node2.value)
			print "-g's|d' = ",PSD
			
	elif node1.letter == "X":
		if node2.letter == "S":
			Cancer = node2.children[0]
			Poll = Cancer.parent[0]
			PXS1 = .9 * 0.03 * (Poll.value) * node2.value
			PXS1 = PXS1 + .2 * (1-0.03) * (Poll.value) * node2.value
			PXS1 = PXS1 + .9 * 0.05 * (1-Poll.value) * node2.value
			PXS1 = PXS1 + .2 * (1-0.05) * (1-Poll.value) * node2.value
			PXS2 = 0.03 * (Poll.value) * node2.value
			PXS2 = PXS2 + (1-0.03) * (Poll.value) * node2.value
			PXS2 = PXS2 + 0.05 * (1-Poll.value) * node2.value
			PXS2 = PXS2 + (1-0.05) * (1-Poll.value) * node2.value
			PXS = PXS1 / PXS2
			print "-g'x|s' = ",PXS
		elif node2.letter == "C":
			node1.condProb.append(0.90)
			node1.condProb.append(0.20)
			print "-g'x|c' = ",node1.condProb[0]
		elif node2.letter == "D":
			print "D"
			
	elif node1.letter == "D":
		if node2.letter == "S":
			Cancer = node2.children[0]
			Poll = Cancer.parent[0]
			PDS1 = .65 * 0.03 * (Poll.value) * node2.value
			PDS1 = PDS1 + .3 * (1-0.03) * (Poll.value) * node2.value
			PDS1 = PDS1 + .65 * 0.05 * (1-Poll.value) * node2.value
			PDS1 = PDS1 + .3 * (1-0.05) * (1-Poll.value) * node2.value
			PDS2 = 0.03 * (Poll.value) * node2.value
			PDS2 = PDS2 + (1-0.03) * (Poll.value) * node2.value
			PDS2 = PDS2 + 0.05 * (1-Poll.value) * node2.value
			PDS2 = PDS2 + (1-0.05) * (1-Poll.value) * node2.value
			PDS = PDS1 / PDS2
			print "-g'd|s' = ",PDS
		elif node2.letter == "C":
			node1.condProb.append(0.65)
			node1.condProb.append(0.3)
			print "-g'd|c' = ",node1.condProb[0]
		elif node2.letter == "D":
			node1.condProb.append(0.65)
			node1.condProb.append(0.3)
			node2.condProb.append(0.65)
			node2.condProb.append(0.3)
			print "-g'd|d' = ",(node1.condProb[0] / node2.condProb[0])
	
def calcJoint(argList,nodeList):
	#-------------------------------------------------------------------
	#Depening on the input, it will calculate the Joint probability,
	#including the Combined from the table.
	#-------------------------------------------------------------------
	print argList,nodeList
	
def main():
	#---------------------------------------
	#Initialize the Nodes of the Bayes Net:
	#---------------------------------------
	C = Node()
	X = Node()
	D = Node()
	P = Node()
	S = Node()
	#-------------------------------------------------------
	#Initialize the properties of the nodes in the network:
	#-------------------------------------------------------
	P.value = 0.90
	S.value = 0.30
	C.parent.append(P)
	C.parent.append(S)
	X.parent.append(C)
	D.parent.append(C)
	P.parent.append(None)
	S.parent.append(None)
	C.children.append(X)
	C.children.append(D)
	X.children.append(None)
	D.children.append(None)
	P.children.append(C)
	S.children.append(C)
	C.letter = "C"
	X.letter = "X"
	D.letter = "D"
	P.letter = "P"
	S.letter = "S"
	#---------------------------------------------------------
	# getopt Code from Rhonda, modified based on my structure
	#---------------------------------------------------------
	try:
		opts, args = getopt.getopt(sys.argv[1:], "m:g:j:p:")
	except getopt.GetoptError as err:
		# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		sys.exit(2)
	for o, a in opts:
		if o in ("-p"):
			print "flag", o
			print "args", a
			print a[0]
			print float(a[1:])
			#setting the prior here works if the Bayes net is already built
			if a[0] == "P":
				node = P
			elif a[0] == "S":
				node = S
			setPrior(node, float(a[1:]))
		elif o in ("-m"):
			print "flag", o
			print "args", a
			if (a == "C") or (a == "c") or (a == "~C") or (a == "~c"):
				node = C
			elif (a == "D") or (a == "d") or (a == "~D") or (a == "~d"):
				node = D
			elif (a == "X") or (a == "x") or (a == "~X") or (a == "~x"):
				node = X	
			elif (a == "P") or (a == "p") or (a == "~P") or (a == "~p"):
				node = P
			elif (a == "S") or (a == "s") or (a == "~S") or (a == "~s"):
				node = S
			print type(a)
			calcMarginal(a, node)
		elif o in ("-g"):
			argList = []
			nodeList = []
			print "flag", o
			print "args", a
			print type(a)
			'''you may want to parse a here and pass the left of |
			and right of | as arguments to calcConditional
			'''
			p = a.find("|")
			argList.append(a[:p])
			argList.append(a[p+1:])
			print a[:p]
			args = a[:p]
			if (args == "C") or (args == "c") or (args == "~C") or (args == "~c"):
				nodeList.append(C)
			elif (args == "D") or (args == "d") or (args == "~D") or (args == "~d"):
				nodeList.append(D)
			elif (args == "X") or (args == "x") or (args == "~X") or (args == "~x"):
				nodeList.append(X)
			elif (args == "P") or (args == "p") or (args == "~P") or (args == "~p"):
				nodeList.append(P)
			elif (args == "S") or (args == "s") or (args == "~S") or (args == "~s"):
				nodeList.append(S)
			print a[p+1:]
			args = a[p+1:]
			if (args == "C") or (args == "c") or (args == "~C") or (args == "~c"):
				nodeList.append(C)
			elif (args == "D") or (args == "d") or (args == "~D") or (args == "~d"):
				nodeList.append(D)
			elif (args == "X") or (args == "x") or (args == "~X") or (args == "~x"):
				nodeList.append(X)
			elif (args == "P") or (args == "p") or (args == "~P") or (args == "~p"):
				nodeList.append(P)
			elif (args == "S") or (args == "s") or (args == "~S") or (args == "~s"):
				nodeList.append(S)
			calcConditional(argList[0], argList[1], nodeList)
		elif o in ("-j"):
			arg = 0
			argList = []
			nodeList = []
			print a[arg]
			while (arg < len(a)):
				if "~" in a[arg]:
					argList.append(a[arg] + a[arg+1])
					arg = arg + 2
				else:
					argList.append(a[arg])
					arg = arg + 1
	
			print "flag", o
			print "args", argList
			for args in argList:
				if (args == "C") or (args == "c") or (args == "~C") or (args == "~c"):
					nodeList.append(C)
				elif (args == "D") or (args == "d") or (args == "~D") or (args == "~d"):
					nodeList.append(D)
				elif (args == "X") or (args == "x") or (args == "~X") or (args == "~x"):
					nodeList.append(X)
				elif (args == "P") or (args == "p") or (args == "~P") or (args == "~p"):
					nodeList.append(P)
				elif (args == "S") or (args == "s") or (args == "~S") or (args == "~s"):
					nodeList.append(S)
			print nodeList
			calcJoint(argList, nodeList)
		else:
			assert False, "unhandled option"

if __name__ == "__main__":
	main()
