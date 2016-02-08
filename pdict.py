
report=[]
		
def g(DTYPE,DEV,SER):
	return locals()
	
data=g(DTYPE='prostream',DEV=10,SER=400)
print data # this returns a dictionary

data2=g(DTYPE='Elextrax',DEV=20,SER=800)

report.append(data)
print report
report.append(data2)
print report
