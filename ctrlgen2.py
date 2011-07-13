#!/usr/bin/python
import os
import sys
import string
import re
import textwrap

thisprogram="ctrlgen2"
version="kino_13JUL_2011"

deco="---"

def RemoveExistedfile(filename):
                flag=os.path.isfile(filename)
                if flag:
                        try:
                                os.remove(filename)
                        except:
                                print "Error: failed to remove file",filename
                                sys.exit(10)
		print "deleted",filename

def Removefile(filename):
		flag=os.path.isfile(filename)
                if flag:
			os.remove(filename)
                print "deleted",filename


def uniq(list):
        result = []
        for l in list:
                if not l in result:
                        result.append(l)
        return result


def GetKeyInSection(key,listsite):
        searchkey="\W"+ key+ "\W*"
        ddd=[]
        for x in listsite:
#               xx=re.split('\WATOM=\W*',x)
                xx=re.split(searchkey,x)
                ddd=ddd+xx[1:]
        rrr=[]
        for i in ddd:
                rrr.append(re.split(' ',i)[0])
        return rrr


def countnum(mmm,key):
        xx2=re.split(key+"\s*",mmm)
        #print 'xx2=',key, xx2
        try:
                xx=re.split(' *',xx2[1])
        except:
                return 0
        num=0
        for i in xx:
                try:
                        yy = float(i)
                        #print yy
                        num=num+1
                except:
                        break
        return num


def is_f_elec(z):
        try:
                z=float(z)
        except:
                i=0
        #print "%f" % z

        # La=57, Lu=71,  Sc=89
        if  (56.5<z and  z<72.5):
                return 1
        if  (z>88.5 ):
                 return 1
        return 0


def Line_Separate(lines):
	"input: list of text, output: list of [text and comment]"
	ans=[]
	for line in lines:
		if re.search("^ *%",line):
			ans.append(Var(line))
			continue

		p=line.find("#")
		if p>=0:
			if p>0:
				#ans.append( line[:p])
				ans.append(Script(line[:p]))
			#ans.append( line[p:])
			ans.append( Comment(line[p:]) )
		else:
			#ans.append(line)
			ans.append( Script(line) )
			
	return ans



def lineReadfile(filename):
        """ read file and make list of the content of the file, and \n->'' """
#       "input:filename output=readlines() "
	try:
        	f = open(filename)
	except:
		print deco,"Failed to open a file",filename
		sys.exit(10)
        list1 =[]
        while 1:
                s = f.readline()
                if s=="":
                        break
                s=string.replace(s,"\n","")
                if s=="":
                        continue
                list1.append(s)
        f.close()
        return list1



def RemoveSection(listctrl,key):
        """ remove a category (key) from listctrl input:devided line, output: devided line"""
        res=[]
        ix=0
        sss ='^('+key.upper()+'|'+key.lower()+')'+'(\s|\Z)'
        for x in listctrl:
                if(ix==1):
                        if(re.match('^\w',x)): ix=0
                if(re.match(sss,x)): ix=1
                if(ix==0): res.append(x)

#       res=res+'\n'
#       print res
#       sys.exit()
        return res

def GetSection(listctrl,key):
        """ get a category (key) from listctrl This returns lines. Not good correspondence to RemoveSection """
        res=[]
        ix=0
        sss ='^('+key.upper()+'|'+key.lower()+')'+'(\s|\Z)'
#       print sss
        for x in listctrl:
#               print x
                if(ix==1):
                        if(re.match('^\w',x)): break
                if(re.match(sss, x )): ix=1
                if(ix==1): res.append(x)

#       res=res+'\n'
#       print res
#       sys.exit()
        return res

def RemoveLines(listctrl,key):
        """ remove lines starting key"""
        res=[]
        ix=0
        sss ='^('+key.upper()+'|'+key.lower()+')'+'(\s|\Z)'
        for x in listctrl:
                if not re.match(sss,x): 
			res.append(x)

        return res

def GetLines(listctrl,key):
        """ get lines staring key"""
        res=[]
        ix=0
        sss ='^('+key.upper()+'|'+key.lower()+')'+'(\s|\Z)'
        for x in listctrl:
                if(re.match(sss, x )): 
			res.append(x)

        return res



def list2Text(a):
	if isinstance(a,list):
        	aaa=''
        	for i in a:
                	aaa=aaa+i+'\n'
	elif isinstance(a,basestring):
		aaa=a
	else:
		print "Error: type unknown ",type(a)
		sys.exit(10)
        return aaa

def list2Text2(a):
	if isinstance(a,list):
        	aaa=''
        	for i in a:
                	aaa=aaa+i+' '
	elif isinstance(a,basestring):
		aaa=a
	else:
		print "Error: type unknown ",type(a)
		sys.exit(10)
        return aaa

def  lines2Token(linein):
        """ convert the result of readline to token """
#       """ input=readlines() output=token""
        listout = []
        for s in linein:
                if s=="":
                        continue
                s = string.replace(s,'\n','')
                s = string.replace(s,',',' ')
                s = string.replace(s,'=',"= ")
                s = string.replace(s,':',": ")

                lista=string.split(s)
                for x in lista:
                        if x<>"":
                                listout.append(x)


        return listout


def make_mixing_string(optionvalues):
	""" mixing sentense ,MIX=A5,b=0.3,n=6 and so on."""

	if optionvalues.mix_a_b_val.Changed()==0 and optionvalues.systype_val.Get()=="molecule":
		b="0.3"
	else:
		b=optionvalues.mix_a_b_val.Get()
	if optionvalues.systype_val.Get()=="molecule":
		a="5"
		n="6"
	else:
		a="2"
		n="3"
	str="MIX=A"+a+",b="+b+",n="+n
	print "mix string:",str
	return str


#--------------------------------------------

class Keyvalues:
	comment=""
	key=""
	values=[]
	def __init__(self):
		comment=""
		self.key=""
		self.values=[]
	def set_comment(self,c):
		self.comment=c
	def set(self,key,values):
		self.key=key
		self.values=values
	def value_append(self,value):
		self.values.append(value)
	def contains(self):
		if len(self.key)>0:
			return 1
		return 0
	def show(self):
		print self.key, self,values
	def __str__(self):
		if len(self.values)>0:
			a="["+self.values[0]
			for i in range(1,len(self.values)):
				a=a+" "	+ self.values[i]
			a=a+"]"
		else:
			a="[]"
		return "key="+self.comment+self.key + ",value=" + a


class Atomsection:
	"input ATOM=V PZ=4 0 Z=50, output: V list[Keyvalues]"
	atom=""
	token=[]
	disableprintlist=[]
	def __init__(self,list):
		self.atom=""
		self.token=[]
		disableprintlist=[]
		self.set_list(list)
	def set_list(self,list):
		"list=string: ATOM=V PZ=4 0 Z=50"
		token=lines2Token([list])
		for i in range(0,len(token)):
			if token[i]=="ATOM=":
				self.atom=token[i+1]
				break	
		if len(self.atom)==0:
			print "Error: atomname not found"
			print "list="
			print list
			sys.exit(10)
		aset=Keyvalues()
		for a in token:
			if re.search("=$",a):
				if aset.contains()>0:
					self.token.append(aset)
				aset=Keyvalues()
				aset.key=a
			else:
				aset.value_append(a)
		if aset.contains()>0:
			self.token.append(aset)


	def overwrite(self, another_Atomsection):
		"token = list [Keyvalues]" 	
		# check type
		flag=0
		if (self.atom==another_Atomsection.atom):
			flag=1	
		if flag==0:
			print "Error: atom is different:", 
			print self.atom,another_Atomsection.atom
			sys.exit(10)
		for token2 in another_Atomsection.token:
			# search token.key
			found=0
			for i in range(0,len(self.token)):
				if token2.key==self.token[i].key:
					found=1
					break
			if found==1:
				self.token[i]=token2
				print "Overwrite",token2
			else:
				self.token.append(token2)
				
			
	def show(self):
		print self.atom,
		#print type(self.token)
		for n in  self.token:
			print n,
		print ""
	def __str__(self):
		#print "(Atomsection.__str__)",
		a="["
		for n in self.token:
			a=a+" "+n.__str__()
		a=a+"]"
		return self.atom+","+ a

	def disable_print(self,str):
		self.disableprintlist.append(str)
		print "disabling ",str, "list=",self.disableprintlist

	def enable_print(self,str):
		newlist=[]
		for key in self.disableprintlist:
			if key==str:
				i=0
			else:
				newlist.append(key)
		self.disableprintlist=newlist
		print "enabling ",str, "list=",self.disableprintlist

	def strlist_ctrlform(self):
		spf="   "
		sp1=" "
		sp ="     "
		a=[]
		str=""
		# copy token
		#token=self.token
		token=[]
		for n in self.token:
			token.append(n)

		# delete token "PZ="
		for delkey in self.disableprintlist:
			for i in range(0,len(token)):
				n=token[i]
				if delkey==n.key:
					token.pop(i)
					break

		print "debug", self.disableprintlist,  "PZ=" in self.disableprintlist
		print "first token"
		for n in token:
			print n
		print "--------"

		
		key="ATOM="
		for i in range(0,len(token)):
			n=token[i]
			if key==n.key:
				str= str+spf+  n.comment+n.key +sp1
                        	for m in n.values:
                                	str=str+  m+sp1
				token.pop(i)
				break
		key="Z="
                for i in range(0,len(token)):
			n=token[i]
                        if key==n.key:
                                str= str+sp1+  n.comment+n.key +sp1
                                for m in n.values:
                                        str=str+  m+sp1
                                token.pop(i)
                                break
		key="R="
		for i in range(0,len(token)):
			n=token[i]
                        if key==n.key:
                                str= str+sp1+  n.comment+n.key +sp1
                                for m in n.values:
                                        str=str+  m+sp1
                                token.pop(i)
                                break
		a.append(str)
		str=""
                key="RSMH="
                for i in range(0,len(token)):
			n=token[i]
                        if key==n.key:
                                str=str+ sp+  n.comment+n.key +sp1
                                for m in n.values:
                                        str=str+  m+sp1
                                token.pop(i)
                                break
                key="EH="
                for i in range(0,len(token)):
			n=token[i]
                        if key==n.key:
                                str= str+sp1+  n.comment+n.key +sp1
                                for m in n.values:
                                        str=str+  m+sp1
                                token.pop(i)
                                break
		a.append(str)
		str=""
                key="RSMH2="
                for i in range(0,len(token)):
			n=token[i]
                        if key==n.key:
                                str=str+ sp+  n.comment+n.key +sp1
                                for m in n.values:
                                        str=str+  m+sp1
                                token.pop(i)
                                break
                key="EH2="
                for i in range(0,len(token)):
			n=token[i]
                        if key==n.key:
                                str= str+sp1+  n.comment+n.key +sp1
                                for m in n.values:
                                        str=str+  m+sp1
                                token.pop(i)
                                break
                a.append(str)
                str=""
                key="KMXA="
                for i in range(0,len(token)):
			n=token[i]
                        if key==n.key:
                                str= str+sp+  n.comment+n.key +sp1
                                for m in n.values:
                                        str=str+  m+sp1
                                token.pop(i)
                                break
                key="LMX="
                for i in range(0,len(token)):
			n=token[i]
                        if key==n.key:
                                str= str+sp1+  n.comment+n.key +sp1
                                for m in n.values:
                                        str=str+  m+sp1
                                token.pop(i)
                                break
                key="LMXA="
                for i in range(0,len(token)):
			n=token[i]
                        if key==n.key:
                                str= str+sp1+  n.comment+n.key +sp1
                                for m in n.values:
                                        str=str+  m+sp1
                                token.pop(i)
                                break
		a.append(str)

		str=""
                key="MMOM="
                for i in range(0,len(token)):
			n=token[i]
                        if key==n.key:
                                str= str+sp+  n.comment+n.key +sp1
                                for m in n.values:
                                        str=str+  m+sp1
                                token.pop(i)
                                break
                a.append(str)
		str=""
                key="Q="
                for i in range(0,len(token)):
			n=token[i]
                        if key==n.key:
                                str= str+sp+  n.comment+n.key +sp1
                                for m in n.values:
                                        str=str+  m+sp1
                                token.pop(i)
                                break
                a.append(str)



                str=""

		for n in token:
			# Keyvalues
			str= sp
			str=str+ n.comment+n.key +sp1
			for m in n.values:
				str=str+  m+sp1
			a.append(str)
		print "ctrlform=",a
		return  a


	def Getvalue(self,key):
		for  n in self.token:
			if key==n.key:
				if (len(n.values)==1):
					return n.values[0]
				else:
					return  n.values
		print "Warning: failed to find key=",key
		return ""
	def SetValue(self,key,values):
		for i in range(0,len(self.token)):
			if self.token[i].key==key:
				self.token[i].values=values
				return
		a=Keyvalues()
		a.set(key,values)
		self.token.append(a)

        def set_comment(self,key,c):
                for  i in range(0,len(self.token)):
			n=self.token[i]
                        if key==n.key:
				self.token[i].comment=c
				return 
                print "Warning: Atomsection.set_comment,  failed to find key=",key
                return 

		
			


class Script:
	text=""
	def __init__(self,text):
		self.text=text
	def __str__(self):
		return self.text
class Comment:
	text=""
	def __init__(self,text):
		self.text=text
	def __str__(self):
		return self.text

class Var:
	text=""
	def __init__(self,text):
		self.text=text
	def __str__(self):
		return self.text


class Atomstd:
	
	__specstd=\
"""
SPEC (standard setting)
  ATOM=H   Z=1  
  ATOM=He  Z=2  
  ATOM=Li  Z=3  
  ATOM=Be  Z=4  
  ATOM=B   Z=5  
  ATOM=C   Z=6  
  ATOM=N   Z=7  
  ATOM=O   Z=8  
  ATOM=F   Z=9  
  ATOM=Ne  Z=10 
  ATOM=Na  Z=11 
  ATOM=Mg  Z=12 
  ATOM=Al  Z=13 
  ATOM=Si  Z=14 
  ATOM=P   Z=15 
  ATOM=S   Z=16 
  ATOM=Cl  Z=17 
  ATOM=Ar  Z=18 
  ATOM=K   Z=19 
  ATOM=Ca  Z=20 
  ATOM=Sc  Z=21 
  ATOM=Ti  Z=22 
  ATOM=V   Z=23 
  ATOM=Cr  Z=24 
  ATOM=Mn  Z=25 
  ATOM=Fe  Z=26 
  ATOM=Co  Z=27 
  ATOM=Ni  Z=28 
  ATOM=Cu  Z=29 
  ATOM=Zn  Z=30 
  ATOM=Ga  Z=31 
  ATOM=Ge  Z=32 
  ATOM=As  Z=33 
  ATOM=Se  Z=34 
  ATOM=Br  Z=35 
  ATOM=Kr  Z=36 
  ATOM=Rb  Z=37 
  ATOM=Sr  Z=38 
  ATOM=Y   Z=39 
  ATOM=Zr  Z=40 
  ATOM=Nb  Z=41 
  ATOM=Mo  Z=42 
  ATOM=Tc  Z=43 
  ATOM=Ru  Z=44 
  ATOM=Rh  Z=45 
  ATOM=Pd  Z=46 
  ATOM=Ag  Z=47 
  ATOM=Cd  Z=48 
  ATOM=In  Z=49 
  ATOM=Sn  Z=50 
  ATOM=Sb  Z=51 
  ATOM=Te  Z=52 
  ATOM=I   Z=53 
  ATOM=Xe  Z=54 
  ATOM=Cs  Z=55 
  ATOM=Ba  Z=56 
  ATOM=La  Z=57 
  ATOM=Ce  Z=58 
  ATOM=Pr  Z=59 
  ATOM=Nd  Z=60 
  ATOM=Pm  Z=61 
  ATOM=Sm  Z=62 
  ATOM=Eu  Z=63 
  ATOM=Gd  Z=64 
  ATOM=Tb  Z=65 
  ATOM=Dy  Z=66 
  ATOM=Ho  Z=67 
  ATOM=Er  Z=68 
  ATOM=Tm  Z=69 
  ATOM=Yb  Z=70 
  ATOM=Lu  Z=71 
  ATOM=Hf  Z=72 
  ATOM=Ta  Z=73 
  ATOM=W   Z=74 
  ATOM=Re  Z=75 
  ATOM=Os  Z=76 
  ATOM=Ir  Z=77 
  ATOM=Pt  Z=78 
  ATOM=Au  Z=79 
  ATOM=Hg  Z=80 
  ATOM=Tl  Z=81 
  ATOM=Pb  Z=82 
  ATOM=Bi  Z=83 
  ATOM=Po  Z=84 
  ATOM=At  Z=85 
  ATOM=Rn  Z=86 
  ATOM=Fr  Z=87 
  ATOM=Ra  Z=88 
  ATOM=Ac  Z=89 
  ATOM=Th  Z=90 
  ATOM=Pa  Z=91 
  ATOM=U   Z=92 
  ATOM=Np  Z=93 
  ATOM=Pu  Z=94 
  ATOM=Am  Z=95 
  ATOM=Cm  Z=96 
  ATOM=Bk  Z=97 
  ATOM=Cf  Z=98 
  ATOM=Es  Z=99 
  ATOM=Fm  Z=100
  ATOM=Md  Z=101
  ATOM=No  Z=102
  ATOM=Lr  Z=103
"""

	__specdic={}

	def __init__(self):
		liststdspec = re.split('\n',self.__specstd)  # SPEC standard if no SPEC is in ctrls.*
		specdat = re.split('\WATOM=\W*',list2Text(liststdspec))[1:]
		self.specdic={}
		for i in specdat:
		        xx=re.split(' *',i)
        		ii=re.sub("\n","",i)
			str='ATOM='+ii
			atomstr=Atomsection(str)
        		self.specdic[xx[0]]= 'ATOM='+ii

	def Getstr(self,str):
		return self.specdic[str]	

class Rmt:
	rdic={}
	__basename="rmt."
	def __init__(self,ext,r_mul_val=1.0):
		self.rdic={}
		filename=self.__basename+ext
		print "Delete",filename
		try:
			os.remove(filename)
		except:
			i=0
		
	def read(self,ext,r_mul_val=1.0):
		filename=self.__basename+ext
		try:
        		listr = lineReadfile(filename)
		except:
        		print ' Error: failed to read file: ',file
        		sys.exit(10)
		self.rdic={}
		for i in listr:
        		xx=re.split(' *',i)
        		self.rdic[xx[0]]= string.atof(xx[1])*string.atof(r_mul_val)
        		self.rdic[xx[0]]= str(self.rdic[xx[0]])
		print "Successfully read the file",filename
	def Getvalue(s):
		return self.rdic[s]


class Mtopara:
	mtodic={}
        __basename="mtopara."
	def __init__(self,ext2):
		file=self.__basename+ext2
		print "Delete",file
		try:
			os.remove(file)
		except:
			i=0

	def read(self,ext2):
		file=self.__basename+ext2
		try:
        		listmto = lineReadfile(file)
		except:
        		print "---> No mtopara."+ext2, "or some problem"
        		sys.exit(10)
		self.mtodic={}
		for i in listmto:
        		i=re.sub("KMXA=","\n    KMXA={kmxa} LMXA=5",i)
        		xx=i.split('@')
        		self.mtodic[xx[0]]= xx[1]
			print "Mtopara",xx[0],xx[1]
		print "Successfully read the file",file

	def show(self):
		print self.mtodic


class Value:
	def __init__(self,value):
		self.value=value
	def Set(self,value):
		self.value=value
	def Get(self):
		return self.value

class ValueOnce:
	def __init__(self,value):
		self.value=value
		self.l=0
	def Changed(self):
		return self.l
	def Set(self,value):
		if self.l==0:
			self.value=value
		self.l =self.l+1
	def Get(self):
		return self.value



class Optionvalues:

	__helpmsg=\
"\nUsage  : "+ thisprogram +" {extension of ctrls file} [option]\n"+"""
 If we supply rmt.tmp by hand with --readrmt, the give rmt.tmp is used."
 The rmt(Muffin-tin radius) are not calculated."
      rmt.tmp consists of specname R with rmt for each line. For example,---"
       --- rmt.tmp for SrTiO3 --- 
       Sr          3.616323
       Ti          2.089960
       O           1.595007
       --- end of rmt.tmp ------- 
 After you write rmt.tmp, do ctrlgen.py again
"""
	def __init__(self):
        	self.nspin_val=ValueOnce("1")
        	self.xcfun_str=ValueOnce("pbe")
        	self.xcfun_val=Value(103)
        	#mmom_val="0 0 0 0"
        	self.r_mul_val=ValueOnce("1.0")
        	self.systype_val=ValueOnce("molecule")
        	self.nk_val=ValueOnce("4")
        	self.readrmt=ValueOnce(0)
		self.eh1=ValueOnce("-0.1")
		self.eh2=ValueOnce("-2.0")
		self.mix_a_b_val=ValueOnce("0.2")
		self.fsmom_val=ValueOnce("")


	def show_options(self):
		msg="""
Options: 
\t--nspin=(1|2) : default=1
\t--xcfun=(pbe|vwn) : default=pbe
\t--r_mul=float_value : default=1.0.  R= 'touching R' * r_mul 
\t--nk=integer_value : default=4.  NKABC= nk nk nk 
\t--systype=(molecule|bulk) : default=molecule
\t--readrmt : default=not set.  read rmt.tmp file
\t--fsmom=float_value : default=not set. the value nk also affects related options.

If systype==molecule, 1: nk=1 if --nk is not set explicitly. 2: ELIND=0. 3: uncomment the TETRA=0 part.
if systype==bulk, 1: ELIND=-1. 2: comment out the TETRA=0 part.

If nk==1; then I set MIX=A5,b=0.3,n=6
"""
		print msg

	def manip_argset(self,argset):
	    	error_title="ARGUMENT ERROR"
    		ierror=0

		for arg in argset:
		    if re.match("--nspin",arg)!=None and re.match("--nspin=",arg)!=None:
		            nspinlist=arg.split("=")
		            if len(nspinlist)==2:
		                    self.nspin_val.Set(nspinlist[1])
		    elif re.match("--xcfun",arg)!=None and re.match("--xcfun=",arg)!=None:
		            xclist=arg.split("=")
		            if len(xclist)==2:
		                    self.xcfun_str.Set(xclist[1])
		    #elif re.match("--mmom",arg)!=None and re.match("--mmom=",arg)!=None :
		    #        mmomlist=arg.split("=")
		    #        if len(mmomlist)==2:
		#		if self.l_mmom_val==0:
		#                    self.mmom_val=mmomlist[1]
		#		    self.l_mmom_val=1
		    elif re.match("--r_mul",arg)!=None and re.match("--r_mul=",arg)!=None:
		            rlist=arg.split("=")
		            if len(rlist)==2:
		                    self.r_mul_val.Set(rlist[1])
		    elif re.match("--nk",arg)!=None and re.match("--nk=",arg)!=None:
		            nklist=arg.split("=")
		            if len(nklist)==2:
		                    self.nk_val.Set(nklist[1])
		    elif re.match("--mixa_b",arg)!=None and re.match("--mixa_b=",arg)!=None:
		            nklist=arg.split("=")
		            if len(nklist)==2:
		                    self.mix_a_b_val.Set(nklist[1])
		    elif re.match("--fsmom",arg)!=None and re.match("--fsmom=",arg)!=None:
		            nklist=arg.split("=")
		            if len(nklist)==2:
		                    self.fsmom_val.Set(nklist[1])
		    elif re.match("--systype",arg)!=None and re.match("--systype=",arg)!=None:
		            syslist=arg.split("=")
		            if len(syslist)==2:
		                    self.systype_val.Set(syslist[1])
		    elif arg=="--help":
		            do_nothing=0
		    elif arg=="--readrmt":
		            self.readrmt.Set(1)
		    elif re.match("-",arg):
		            sys.stderr.write( error_title + ", unknown arg:  "+arg+"\n")
		            ierror+=1
		if self.xcfun_str.Get().upper()=="PBE":
		    self.xcfun_val.Set("103")
		elif self.xcfun_str.Get().upper()=="VWN":
		    self.xcfun_val.Set("1")
		else:
		    sys.stderr.write(error_title+", --xc="+self.xcfun_str.Get()+" : unknown\n")
		    ierror+=1

		if self.systype_val.Get().upper()=="MOLECULE":
		    do_nothing=0
		    self.nk_val.Set("1")
		elif self.systype_val.Get().upper()=="BULK":
		    do_nothing=0
		else:
		    sys.stderr.write(error_title+", --systype="+self.systype_val.Get()+" : unknown\n")
		    ierror+=1


		if ierror!=0:
		    self.show_help()
		    print "ABORT"
		    sys.exit(-1)

	def show_help(self):
		print "Generating ctrl.{ext} file from ctrls.{ext} ;", version
		print self.__helpmsg
		self.show_options()


	def show(self):
		if 1:
		    print "options:",
		    print " nspin_val=",self.nspin_val.Get(),
		    print " xcfun_val=",self.xcfun_val.Get(),
		    #print "mmom_val=",self.mmom_val
		    #print "r_mul_val=",self.r_mul_val.Get()," float=",float(self.r_mul_val.Get())
		    print " r_mul_val=",self.r_mul_val.Get(),
		    print " systype_val=",self.systype_val.Get(),
		    print " readrmt=",self.readrmt.Get()


class  Ctrlfile:
	sitesection=[]
	specsection=[]
	strucsection=[]
	lines=[]
	ansite=0
	anspec=0
	__atomstd=""
	__rmt=""
	__mtopara=""
        __ctrlcontents=""
	__head1="### This is generated by ctrlgen2.py from ctrls ;" + version 
	__head2="""
### For tokens, See http://titus.phy.qub.ac.uk/packages/LMTO/tokens.html. 
### However, lm7K is now a little different from Mark's lmf package in a few points.
### Do lmf --input to see all effective category and token ###
### It will be not so difficult to edit ctrlge.py for your purpose ###
VERS    LM=7 FP=7
             # version check. Fixed.

IO      SHOW=T VERBOS=35
             # SHOW=T shows readin data (and default setting at the begining of console output)
             # It is useful to check ctrl is read in correctly or not (equivalent with --show option).
             #
             # lerger VERBOSE gives more detailed console output.

SYMGRP find  # 'find' evaluate space-group symmetry automatically.
             # Usually 'find is OK', but lmf may use lower symmetry
             # because of numerical problem.
             # Do lmchk to check how it is evaluated.
             # See http://titus.phy.qub.ac.uk/packages/LMTO/tokens.html#SYMGRPcat
             
%const kmxa=5  # kmxa=5 is good for pwemax=3 or lower.
               # larger kmxa is better but time-consuming. A rule of thumb: kmxa>pwemax in Ry.\n
"""
	
	def __init__(self,matext,argset,optionvalues):

		file="ctrls."+matext
		if not isinstance(optionvalues,Optionvalues):
			print "Internal error: argument error in Ctrlfile.__init__"
			sys.exit(10)

		try:
			self.lines=lineReadfile(file)
		except:
			print "failed to read file:",file
			sys.exit(10)

		str=""
		for n in argset:
			str=str+" "+n
		self.lines.insert(0,"#commandlinearguments "+str)

                self.ctrlgensection=GetLines(self.lines,"#ctrlgen")
                #self.lines=RemoveLines(self.lines,"#ctrlgen")
                optstrlist=[]
                for n in self.ctrlgensection:
                        s=re.sub("^#ctrlgen ","",n)
                        slist=re.split(" *",s)
                        for m in slist:
                                optstrlist.append(m)
                optionvalues.manip_argset(optstrlist)
		optionvalues.show()


		self.sitesection=GetSection(self.lines,"SITE")
		self.lines=RemoveSection(self.lines,"SITE")

		self.strucsection=GetSection(self.lines,"STRUC")
		self.lines=RemoveSection(self.lines,"STRUC")

		self.specsection=GetSection(self.lines,"SPEC")
		self.lines=RemoveSection(self.lines,"SPEC")
		self.specsection=Line_Separate(self.specsection)
		# use only Script
		str=[]
		for n in self.specsection:
		    if isinstance(n,Script):
			str.append(n.text)
		str=re.split('\WATOM=\W*',list2Text(str)) [1:]
		str2=[]
		for a in str:
			str2.append("ATOM= "+string.replace(a,"\n",""))
		self.specsection=str2

		for i in range(0,len(self.specsection)):
			str= self.specsection[i]
			self.specsection[i]=Atomsection(str)


		# add Z=
                #self.__atomstd=Atomstd()
                #for i in range(0,len(self.specsection)):
                #        atomsection= self.specsection[i]
                #        if isinstance(atomsection,Atomsection):
                #                stdstr=self.__atomstd.Getstr(atomsection.atom)
                #                print "stdstr=",stdstr
                #                stdatom=Atomsection(stdstr)
                #                stdatom.overwrite(atomsection)
                #                self.specsection[i]=stdatom

		#------- step1, find R ------------
		ext="tmp"
		self.__rmt=Rmt(ext)
		self.step1(optionvalues)
		self.__rmt.read(ext,optionvalues.r_mul_val.Get())
		#------ step2, mtopara------------
		ext="tmp2"
		self.__mtopara=Mtopara(ext)
		self.step2(ext,optionvalues)
		self.__mtopara.read(ext)
		#------- step3, new ctrl file ------------
		self.step3(matext,optionvalues)


	def step1(self,optionvalues):
		#site numbers and spec numbers
		print deco,"Step1: trying to find R."
		sitename=GetKeyInSection("ATOM=",self.sitesection)
		print "sitename=",sitename
		self.ansite = '%i' % len(sitename)
		self.anspec = '%i' % len(uniq(sitename))
		if self.ansite==0 or  self.anspec==0:
			print "Error: site number or spec number is zero. ",
			print  self.ansite, self.anspec
			sys.exit(10)

		sitename=uniq(sitename)
		print "uniq sitename=",sitename

		# make list of spec.atom
		specatoms=[]
		for a_spec in self.specsection:
			name=a_spec.Getvalue("ATOM=")
			print "s_spec.Getvalue=",name
			specatoms.append(name)
		
		# add sitename if it is not found in specsection
		for name in sitename:
			if  not name in specatoms:
				aspec_str="ATOM= "+name
				aspec=Atomsection(aspec_str)
				self.specsection.append(aspec)

                # add Z=
                self.__atomstd=Atomstd()
                for i in range(0,len(self.specsection)):
                        atomsection= self.specsection[i]
                        if isinstance(atomsection,Atomsection):
                                stdstr=self.__atomstd.Getstr(atomsection.atom)
                                print "stdstr=",stdstr
                                stdatom=Atomsection(stdstr)
                                stdatom.overwrite(atomsection)
                                self.specsection[i]=stdatom


		print "self.specsection=",len(self.specsection)
		for aspec in self.specsection:
			aspec.show()
		

		head = self.__head1 +self.__head2
		all= head + list2Text(self.lines) \
		+ list2Text(self.strucsection)  + "  NBAS= "+ self.ansite + "  NSPEC="+ self.anspec +'\n' \
         	+ list2Text(self.sitesection) \
         	+ 'SPEC\n'

		print "self.specsection:=",self.specsection

		for n in self.specsection:
		    if isinstance(n,Atomsection):
			a= n.strlist_ctrlform()
			for m in a:
				all = all + m + "\n"
		    else:
			all=all+n.__str__()+"\n"


		#open a file
		ext="tmp"
		inputfilename="ctrl."+ext
		RemoveExistedfile(inputfilename)
		print deco,"Making a temporary file", inputfilename
		try:
			file=open(inputfilename,"wt")
			file.write(all)
			file.close()
		except:
			print "Error: failed to make",inputfilename
			sys.exit(10)
		
		returncodefile="__RETURNCODE__"

		outputfile="llmchk_getwsr"
		iexit=0
		if (optionvalues.readrmt.Get()==0):
		    Removefile(returncodefile)
		    Removefile(outputfile)
		    cmd="lmchk --getwsr "+ext+" > "+outputfile+"; echo $? >"+returncodefile
		    print deco,"Running (", cmd,")"
		    try:
			os.system(cmd)
		    except OSError, e:
			print "Error: Failed to run ",cmd 
			sys.exit(10)

		    # read returncode
		    print deco,"Checking returncode"
		    try:
			file=open(returncodefile,'rt')
		    except:
			print "Error: Failed to open ", returncodefile
			sys.exit(10)
		    iexit=int(file.read())
		    file.close()
		    if iexit==0:
			print deco,"Sucessfully done, and continue."
		    else:
			print "ERROR: failed to execute the previous command, returncode=",iexit
			print "You may find the reason by checking the files ",inputfilename,"and" , outputfile
			sys.exit(10)

		else:
			iexit=2



	def step2(self,ext,optionvalues):

		# add R=
		print deco,"Step2: adding R= in spec section"
                for i in range(0,len(self.specsection)):
                        atomsection= self.specsection[i]
			print "atomsection=",atomsection
                        if isinstance(atomsection,Atomsection):
				str="ATOM="+atomsection.atom+" "
                                stradd=self.add_spec_R(atomsection.atom,self.__rmt.rdic)
				atomadd=Atomsection(str+" "+stradd)
				print "str=",atomadd
				#atomsection.overwrite(atomadd)
				atomadd.overwrite(atomsection)
				self.specsection[i]=atomadd
		
                head = self.__head1 +self.__head2
                all= head + list2Text(self.lines) \
                + list2Text(self.strucsection)  + "  NBAS= "+ self.ansite + "  NSPEC="+ self.anspec +'\n' \
                + list2Text(self.sitesection) \
                + 'SPEC\n'
		
		# PZ must be deleted in order to make lmfa mtopara 
		for n in self.specsection:
		    if isinstance(n,Atomsection):
			n.disable_print("PZ=")	

                for n in self.specsection:
		    if isinstance(n,Atomsection):
                        a= n.strlist_ctrlform()
                        for m in a:
                                all = all + m + "\n"
		    else:
			all=all+n.__str__()+"\n"

		
		all = all + "\nHAM XCFUN="+ optionvalues.xcfun_val.Get()+"\n"
		
		inputfile="ctrl."+ext	
		RemoveExistedfile(inputfile)
		print deco,"Making a temporary file",inputfile
		try:
			file=open(inputfile,"wt")
			file.write(all)
			file.close()
		except:
			print "Error: failed to make",inputfile
			sys.exit(10)

		outputfile="llmfa."+ext
		returncodefile="__RETURNCODE__"
		RemoveExistedfile(outputfile)
		RemoveExistedfile(returncodefile)
		
		cmd="lmfa "+ext+" > "+outputfile+"; echo $? >"+ returncodefile
		print deco,"Running (",cmd ,")"
		try:
			os.system(cmd)
		except OSError, e:
			print "Error: failed to run ",cmd
                        sys.exit(10)

                 # read returncode
                print deco,"Checking returncode"
                try:
                        file=open(returncodefile,'rt')
                except:
                        print "Error: failed to open ", returncodefile
                        sys.exit(10)
                iexit=int(file.read())
                file.close()
                if iexit==0:
                        print deco,"Sucessfully done, and continue."
                else:
                        print "ERROR: failed to execute the previous command, returncode=",iexit
                        print "You may find the reason by checking the files.",inputfile,"and" , outputfile
                        sys.exit(10)
	
		
		

	def step3(self,ext,optionvalues):

		#--- fix spec 
		print deco,"Step3: making a complete ctrl file."
		# load atomstd
		self.__atomstd=Atomstd()
                for i in range(0,len(self.specsection)):
                        atomsection= self.specsection[i]
			if isinstance(atomsection,Atomsection):
				stdstr=self.__atomstd.Getstr(atomsection.atom)
				print "stdstr=",stdstr
				stdstradd=self.add_spec(atomsection, self.__mtopara.mtodic,self.__atomstd,self.__rmt.rdic,optionvalues)
				print "stdstradd=",stdstradd
				stdstr=stdstr+stdstradd
				stdatom=Atomsection(stdstr)
				stdatom.set_comment("Q=","#")
				stdatom.show()
				stdatom.overwrite(atomsection)
				self.specsection[i]=stdatom

                head = self.__head1 +self.__head2
                all= head + list2Text(self.lines) \
                + list2Text(self.strucsection)  + "  NBAS= "+ self.ansite + "  NSPEC="+ self.anspec +'\n' \
                + list2Text(self.sitesection) \
                + 'SPEC\n'

		for n in self.specsection:
		    if (isinstance(n,Atomsection)):
			n.enable_print("PZ=")
                for n in self.specsection:
		    if isinstance(n,Atomsection):
                        a= n.strlist_ctrlform()
                        for m in a:
                                all = all + m + "\n"
		    else:
			all = all + n.__str__() + "\n"

		tail=self.add_tail(optionvalues)
		all=all+tail

		filename="ctrlgen.ctrl."+ext
		file=open(filename,"wt")
		file.write(all)
		file.close()
		print deco,"Sucessfully generated the ctrlfile",filename


	def add_tail(self,optionvalues):
		tail="\n"

		if (optionvalues.systype_val.Get().upper()=="BULK") :
			tail = tail+ "% const pwemax=2 nk="+optionvalues.nk_val.Get()+" nit=30 gmax=12 "
		else:
			tail = tail+ "% const pwemax=2 nk="+optionvalues.nk_val.Get()+" nit=30 gmax=12 "
		tail = tail + "        nspin="+optionvalues.nspin_val.Get()+"\n"

		tail = tail + """BZ    NKABC={nk} {nk} {nk}  # division of BZ for q points.
      METAL=3   # METAL=3 is safe setting. For insulator, METAL=0 is good enough.
		# When you plot dos, set SAVDOS=T and METAL=3, and with DOS=-1 1 (range) NPTS=2001 (division) even for insulator.
		#   (SAVDOS, DOS, NPTS gives no side effect for self-consitency calculaiton).
                # 
                #BUG: For a hydrogen in a large cell, I(takao) found that METAL=0 for
                #(NSPIN=2 MMOM=1 0 0) results in non-magnetic solution. Use METAL=3 for a while in this case.
                # 

      BZJOB=0	# BZJOB=0 (including Gamma point) or =1 (not including Gamma point).
		#  In cases , BZJOB=1 makes calculation efficient.


      #Setting for molecules. No tetrahedron integration. (Smearing))
      # See http://titus.phy.qub.ac.uk/packages/LMTO/tokens.html
"""
		if (optionvalues.systype_val.Get().upper()=="BULK") :
			tail =  tail + """      #TETRA=0 
      #N=-1    #Negative is Fermi distribution function W= gives temperature.
      #W=0.001 #This corresponds to T=157K as shown in console output
               #W=0.01 is T=1573K. It makes stable nonvergence for molecule. 
               #Now you don't need to use NEVMX in double band-path method,
               #which obtain only eigenvalues in first-path to obtain integration weights
               #, and accumulate eigenfunctions in second path.
"""
		else :
			tail =  tail + """      TETRA=0 
      N=-1    #Negative is Fermi distribution function W= gives temperature.
      W=0.001 #This corresponds to T=157K as shown in console output
               #W=0.01 is T=1573K. It makes stable nonvergence for molecule. 
               #Now you don't need to use NEVMX in double band-path method,
               #which obtain only eigenvalues in first-path to obtain integration weights
               #, and accumulate eigenfunctions in second path.
"""


		tail = tail + """      #For Molecule, you may also need to set FSMOM=n_up-n_dn, and FSMOMMETHOD=1 below.
"""
		if optionvalues.fsmom_val.Changed()==0:
			tail= tail + "      #FSMOM=real number (fixed moment method)"
		else:
			tail = tail+ "      FSMOM="+optionvalues.fsmom_val.Get()

		tail = tail + """      #  Set the global magnetic moment (collinear magnetic case). In the fixed-spin moment method, 
      #  a spin-dependent potential shift is added to constrain the total magnetic moment to value 
      #  assigned by FSMOM=. Default is NULL (no FSMOM). FSMOM=0 works now (takao Dec2010)
      #
"""
		if optionvalues.fsmom_val.Changed()!=0:
		    if optionvalues.systype_val.Get()=="molecule":
			tail = tail +"      FSMOMMETHOD=1"
		    else:
			tail = tail + "     FSMOMMETHOD=0"
		else:
			tail = tail + "      #FSMOMMETHOD=0" 

		tail = tail + """   #only effective when FSMOM exists. #Added by t.kotani on Dec8.2010
      #  =0: original mode suitable for solids.(default)
      #  =1: discrete eigenvalue case. Calculate bias magnetic field from LUMO-HOMO gap for each spins.
      #      Not allowed to use together with HAM_SO=1 (L.S). 
      #      It seems good enough to use W=0.001. Smaller W= may cause instability.

      #For Total DOS.   DOS:range, NPTS:division. We need to set METAL=3 with default TETRA (no TETRA).
      #SAVDOS=T DOS=-1 1 NPTS=2001

      #EFMAX= (not implemented yet, but maybe not so difficult).            


      #  See http://titus.phy.qub.ac.uk/packages/LMTO/tokens.html#HAMcat for tokens below.

      #NOINV=T (for inversion symmetry)
      #  Suppress the automatic addition of the inversion to the list of point group operations. 
      #  Usually the inversion symmetry can be included in the determination of the irreducible 
      #  part of the BZ because of time reversal symmetry. There may be cases where this symmetry 
      #  is broken: e.g. when spin-orbit coupling is included or when the (beyond LDA) 
      #  self-energy breaks time-reversal symmetry. In most cases, lmf program will automatically 
      #  disable this addition in cases that knows the symmetry is broken
      #

      #INVIT=F
      #  Enables inverse iteration generate eigenvectors (this is the default). 
      #  It is more efficient than the QL method, but occasionally fails to find all the vectors. 
      #   When this happens, the program stops with the message:
      #     DIAGNO: tinvit cannot find all evecs
      #   If you encounter this message set INVIT=F.
      #  T.Kotani think (this does not yet for lm7K).
"""
		mix_string=make_mixing_string(optionvalues)
		tail = tail + "ITER "+mix_string+" CONV=1e-6 CONVC=1e-6 NIT={nit}"
		tail = tail + """
#ITER MIX=B CONV=1e-6 CONVC=1e-6 NIT={nit}
                # MIX=A: Anderson mixing.
                # MIX=B: Broyden mixing (default). 
                #        Unstable than Anderson mixing. But faseter. It works fine for sp bonded systems.
                #  See http://titus.phy.qub.ac.uk/packages/LMTO/tokens.html#ITERcat

HAM   NSPIN={nspin}   # Set NSPIN=2 for spin-polarize case; then set SPEC_MMOM (initial guess of magnetic polarization).
      FORCES=0  # 0: no force calculation, 1: forces calculaiton 
      GMAX={gmax}   # this is for real space mesh. See GetStarted. (Real spece mesh for charge density).
                # Instead of GMAX, we can use FTMESH.
                # You need to use large enough GMAX to reproduce smooth density well.
                # Look into sugcut: shown at the top of console output. 
                # It shows required gmax for given tolelance HAM_TOL.
      REL=T     # T:Scaler relativistic, F:non rela.
"""
		tail = tail + "     XCFUN=" + optionvalues.xcfun_val.Get() + """
          # =1 for VWN.
                # =2 Birth-Hedin (if this variable is not set).
		#    (subs/evxc.F had a problem when =2 if rho(up)=0 or rho(down)=0).
                # =103 PBE-GGA

      PWMODE=11 # 10: MTO basis only (LMTO) PW basis is not used.
                # 11: APW+MTO        (PMT)
                # 12: APW basis only (LAPW) MTO basis is not used.

      PWEMAX={pwemax} # (in Ry). When you use larger pwemax more than 5, be careful
                      # about overcompleteness. See GetStarted.
"""
		if (optionvalues.systype_val.Get().upper()=="BULK") :
			tail = tail + """      ELIND=-1    # this is to accelarate convergence. Not affect to the final results.
"""
		else :
			tail =  tail + """      ELIND=0    # this is to accelarate convergence. Not affect to the final results.
"""
	
		tail = tail + """                 # For sp-bonded solids, ELIND=-1 may give faster convergence.
                 # For O2 molecule, Fe, and so on, use ELIND=0(this is default).
  
      #STABILIZE=1e-10 #!!! Test option for convergence check. Not tested well.
                       # default is negative, then STABILIZER in diagonalization is not effective 
                       # (See slatsm/zhev.F delta_stabilize).
                       # I am not sure wether this stabilizer works OK or not(in cases this gives little help).
                       # STABILIZE=1e-10 may make convergence stabilized 
                       # (by pushing up poorly-linear-dependent basis to high eigenvalues).
                       # STABILIZE=1e-8 may give more stable convergence. 
                       # If STABILIZE is too large, it may affect to low eigenvalues around E_Fermi

      #FRZWF=T #to fix augmentation function. 
      #  See http://titus.phy.qub.ac.uk/packages/LMTO/tokens.html#HAMcat

      #For LDA+U calculation, see http://titus.phy.qub.ac.uk/packages/LMTO/fp.html#ldaplusu

      #For QSGW. you have to set them. Better to get some samples.
      #RDSIG=
      #RSRNGE=
               
OPTIONS PFLOAT=1 
        # Q=band (this is quit switch if you like to add)

# Relaxiation sample
#DYN     MSTAT[MODE=5 HESS=T XTOL=.001 GTOL=0 STEP=.015]  NIT=20
# See http://titus.phy.qub.ac.uk/packages/LMTO/tokens.html#DYNcat

"""
		return tail


	def add_spec_R(self,ikey,rdic):
                rmt = min(string.atof(rdic[ikey]),3.0)
                rsmh = max(rmt*1.0/2.0,0.5)
                rmt= '%6.3f' % rmt
		aaa="R="+rmt
		return aaa

	def add_spec(self,atomsection,mtodic,atomstd,rdic,optionvalues):
		aaa=""
		ikey=atomsection.atom
		
		print mtodic,ikey
		mmmx=mtodic[ikey]
		mmm=re.sub(","," ",mmmx)
		#il1 = countnum(mmm,'RSMH=')
		il1=4
		atomsec=Atomsection(atomstd.Getstr(ikey))
		pzatom=atomsection.Getvalue("PZ=")
		#pzatom=list2Text2(pzatom)
		#print "pz=",list2Text(pzatom)
		z=atomsec.Getvalue("Z=")
		print "z=",z
		if is_f_elec(z)==1:
		        print "this is a f-electron system."
		        il1=5
		        optionvalues.mix_a_b_val.Set("0.05")
		
		pz=re.split("PZ",mmmx)
		#Over ride by new setting
		rmt=atomsection.Getvalue("R=")
		if len(rmt)>0:
			rmt=float(rmt)
		else:
			rmt = min(string.atof(rdic[ikey]),3.0)
		rsmh = max(rmt*1.0/2.0,0.5)
		rsmh= '%6.3f' % rsmh
		mmm= 'RSMH=  '          +il1*rsmh+' EH=  '+il1*(optionvalues.eh1.Get()+' ')+'\n' #-1 and -0.5 which is better? 
		mmm= mmm+ '     RSMH2= '+il1*rsmh+' EH2= '+il1*(optionvalues.eh2.Get()+' ')+'\n'
		#overwrite PZ= if PZ= is defined in ctrls.* 
		print "len(pzatom)=",len(pzatom)
		if ( len(pzatom)>0 ) :
			il2=len(pzatom)
			mmm= mmm+ '   PZ='+list2Text2(pzatom)
		else:
			if(len(pz)==2): mmm= mmm +'     PZ'+pz[1]
			il2 = countnum(mmm,'PZ=')
		print "il2=",il2,"mmm=",mmm
		lx = max(il1,il2)
		lll = "%i" % lx
		il1m=il1-1
		lmx = "%i" % il1m
		rmt = '%6.3f' % rmt
		#print il1,il2,lx
		aaa = aaa+' R='+rmt +'\n'+' '*5+mmm \
		    +' '*5+'KMXA={kmxa} '+' LMX='+lmx+' LMXA='+lll+'\n'  \
		    +'     MMOM= 0 0 0 0 \n'+'     Q= \n'  
		 #   +'     MMOM= '+optionvalues.mmom_val+' \n'+'     Q= \n'  
		  #  +'     #MMOM and Q are to set electron population. See conf: in lmfa output\n'
		return aaa	

	# for debug use
	def show(self):
		for n in self.lines:
			print n
		for n in self.sitesection:
			print n
		for n in self.strucsection:
			print n
		print "SPEC"
		for n in  self.specsection:
			if isinstance(n,Atomsection):
				for m in n.strlist_ctrlform():
					print m
			else:
				print n


class Main:

	def doit(self):
		optionvalues=Optionvalues()
		argset=set(sys.argv[1:])
		narg= len(argset)
		flag=0
		if narg==0:
			flag=1
		else:
			ext=sys.argv[1]
			if len(ext)==0:
				flag=1
		if flag!=0:
			optionvalues.show_help()
			sys.exit(10)

		optionvalues.manip_argset(argset)
		#optionvalues.show()

		ctrl=Ctrlfile(ext,argset,optionvalues)

#---------main--------------------

main=Main()
main.doit()

