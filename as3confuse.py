#python2
#coding:utf-8

import sys
import os
import re
import random
import shutil

from words import randDict

class RandomAS3(object):
	
	@staticmethod
	def rateArray(num,max):
		vals = []
		idx=0
		while len(vals) < num:
			idx = max
			while idx>0 and len(vals) < num:
				idx-=1
				vals.append(idx)
		resu = []
		while len(vals) > 0:
			idx = random.randint(0,len(vals)-1)
			resu.append(vals[idx])
			del vals[idx]
		return resu
		
	@staticmethod
	def boolean(rat=0.5):
		return random.random()>rat
		
class EmptyFunction(object):
	def __init__(self,code,clas):
		self.code=code
		self.clas=clas
		self.level=self.code.level_fun
		self.rows=[]
		self.returnNotVoid = RandomAS3.boolean()
		self.returnType = "void"
		self.returnType000 = self.returnType
		if self.returnNotVoid:
			self.returnType = random.choice(AS3Function.DATA_TYPE)
			self.returnType000 = self.returnType
			if self.returnType == "Class":
				self.returnType = self.code.getRandomClassUnderLevel(self.clas.level).name
		self.isParameter = False
		# self.parameter = None
		
	def out(self):
		t_rowStr = ''
		for item in self.rows:
			t_rowStr += item.out() + '\n'
		return t_rowStr.rstrip()
		
class AS3CodeRow(object):
	DATA_TYPE = ["String", "int", "Boolean", "Class"]
	DATA_TYPE2 = ["String", "int", "Boolean"]
	# CODE_TYPE = ["const", "var", "function"]#去掉const，因为const在catch语句内不合法
	# CODE_TYPE2 = ["const", "var"]
	CODE_TYPE = ["var", "function"]
	CODE_TYPE2 = ["var"]
	
	def __init__(self, t_func):
		self.fun = t_func
		self.clas=self.fun.clas
		self.code=self.clas.code
		self.codeValue=None
		self.codeName=None
		self.codeDataType=None
		self.codeClass=None
		
	def initWithReturn(self):
		for item in self.fun.rows:
			if item.codeDataType == self.fun.returnType:
				self.codeValue = "return " + item.codeName
				break
		if not self.codeValue:
			if self.fun.returnType == "String":
				self.codeValue = "return " + self.StringValue()
			elif self.fun.returnType == "int":
				self.codeValue = "return " + self.IntValue()
			elif self.fun.returnType == "Boolean":
				self.codeValue = "return " + random.choice(['true','false'])
			else:
				self.codeValue = "return new " + self.fun.returnType + "()"
		
	def initWithNotReturn(self):
		self.codeType = random.choice(AS3CodeRow.CODE_TYPE)
		if self.clas.level == 0 or self.fun.level == 0:
			self.codeType = random.choice(AS3CodeRow.CODE_TYPE2)
			
		if self.codeType == "var": 
			self.codeName = randDict.getProto()
			self.codeValue = "var " + self.codeName + self.initValue()
			self.nextVar()
			if self.clas.level>0:#Xue
				self.next()
		elif self.codeType == "const": 
			self.codeName = randDict.getProto()
			self.codeValue = "const " + self.codeName + self.initValue()
			if self.clas.level>0:#Xue
				self.next()
		elif self.codeType == "function": 
			self.codeValue = self.func()
		
	def out(self):
		return "\t\t\t" + self.codeValue
	
	def func(self):
		t_str = ""
		localFun = RandomAS3.boolean()
		t_fun=None
		t_parameter=""
		if localFun:
			funs = self.clas.getFunctionsUnderLv(self.fun.level)
			t_fun = random.choice(funs)
			#if t_fun.name == self.fun.name:#Xue
				#return func();
			#}
			if t_fun==self.fun:#Xue
				return self.func()

			if t_fun.returnNotVoid:
				return self.func()
			if not t_fun.isParameter:
				t_str = t_fun.name + "()"
			else:
				t_parameter = ""
				for item in t_fun.parameter:
					if item[1] == "String":
						t_parameter += self.StringValue() + ","
					elif item[1] == "int":
						t_parameter += self.IntValue() + ","
					elif item[1] == "Boolean":
						t_parameter += self.BoolValue() + ","
					else:
						t_parameter += "new " + item[1] + "()" + ","
				
				t_str = t_fun.name + "(" + t_parameter[0:-1] + ")"
		else:
			t_arr = self.code.getFunsNotVoid(self.clas.level)
			t_fun = random.choice(t_arr)[0]
			# if t_fun.name == self.fun.name:
				# return self.func()
			if t_fun==self.fun:#Xue
				return self.func()
			if not t_fun.isParameter:
				# t_str = self.code.doc + "." + t_fun.clas.name.lower() + "." + t_fun.name + "()"
				t_str = t_fun.clas.name + "." + t_fun.clas.staticVar.name + "." + t_fun.name + "()"
			else:
				t_parameter = ""
				for item in t_fun.parameter:
					if item[1] == "String":
						t_parameter += self.StringValue() + ","
					elif item[1] == "int":
						t_parameter += self.IntValue() + ","
					elif item[1] == "Boolean":
						t_parameter += self.BoolValue() + ","
					else:
						t_parameter += "new " + item[1] + "()" + ","
				
				# t_str = self.code.doc + "." + t_fun.clas.name.lower() + "." + t_fun.name + "(" + t_parameter[0:-1] + ")"
				t_str = t_fun.clas.name + "." + t_fun.clas.staticVar.name + "." + t_fun.name + "(" + t_parameter[0:-1] + ")"
		return t_str+";"
	
	def initValue(self):
		self.codeDataType = random.choice(AS3CodeRow.DATA_TYPE)
		if self.codeDataType == "Class":
			if self.clas.level==0:
				self.codeDataType = random.choice(AS3CodeRow.DATA_TYPE2)
			else:
				self.codeClass = self.code.getRandomClassUnderLevel(self.clas.level)#Xue
		
		if self.codeDataType == "String": 
			return ": String = " + self.StringValue() + ";"
		elif self.codeDataType == "int": 
			return ": int = " + self.IntValue() + ";"
		elif self.codeDataType == "Boolean": 
			return ": Boolean = " + self.BoolValue() + ";"
		elif self.codeDataType == "Class": 
			return ": " + self.codeClass.name + " = new " + self.codeClass.name + "();"
		
		return ""
	
	def next(self):
		#本类调用函数赋值用
		funs = self.clas.getFunctionsUnderLv(self.fun.level)
		if RandomAS3.boolean():
			for item in funs:
				if item.isParameter and not item.returnNotVoid:
					t_arr = item.parameter
					for idx,arr in enumerate(t_arr):
						if arr[1] == self.codeDataType:
							self.cre(item, idx)
							return
			self.next()
		else:#其他类赋值
			tureType=self.codeDataType
			if self.codeDataType == "Class":
				tureType=self.codeClass.name
			t_list = self.code.getFuns(tureType, self.clas.level)
			if len(t_list)>0:
				t_obj = random.choice(t_list)[0]
				t_arr = t_obj[1].parameter
				for idx,item in enumerate(t_arr):
					if item[1] == self.codeDataType:
						self.cre(t_obj[1], idx, True)
						return
		
		if self.codeDataType == "Class":
			t_v = self.codeClass.getFuncPublicByNotVoid()
			if len(t_v)>0:
				t_fun = random.choice(t_v)
				t_scc = ""
				if t_fun.isParameter:
					for item in t_fun.parameter:
						if item[1] == "String":
							t_scc += self.StringValue() + ","
						elif item[1] == "int":
							t_scc += self.IntValue() + ","
						elif item[1] == "Boolean":
							t_scc += self.BoolValue() + ","
						else:
							t_value = self.globalVaribleValue(item[1])
							if t_value == "":
								t_scc += "new " + item[1] + "()" + ","
							else:
								t_scc += t_value + ","
					t_scc = t_scc[0:-1]
				self.codeValue += "\n\t\t\t" + self.codeName + "." + t_fun.name + "(" + t_scc + ");"
	
	def nextVar(self):
		t_str = ""
		if self.codeDataType == "String": 
			t_str = self.StringValue() + ";"
		elif self.codeDataType == "int": 
			t_str = self.IntValue() + ";"
		elif self.codeDataType == "Boolean": 
			t_str = self.BoolValue() + ";"
		elif self.codeDataType == "Class": 
			t_str = self.codeClass.name + "();"
			return
		
		self.codeValue = self.codeValue + "\n\t\t\t" + self.codeName + " = " + t_str
	
	def cre(self, t_fun, index, t_global = False):
		t_str = ""
		t_arr = t_fun.parameter
		for idx,item in enumerate(t_arr):
			if idx == index:
				t_str += self.codeName + ","
			else:
				t_list = self.clas.getVariableByType(item[1])
				if len(t_list)>0:
					t_str += random.choice(t_list)[1].name + ","
				else:
					t_list2 = self.code.getVariable(item[1],self.clas.level)
					if len(t_list2)>0:
						t_class = random.choice(t_list2)
						# t_str += self.code.doc + "." + t_class[0][0].name.lower() + "." + t_class[0][1].name + ","
						t_str += t_class[0][0].name + "." + t_class[0][0].staticVar.name + "." + t_class[0][1].name + ","
					else:
						t_str += "new " + item[1] + "(),"
		
		t_str = t_str[0:-1]
		
		if t_global:
			# self.codeValue += "\n\t\t\t" + self.code.doc + "." + t_fun.clas.name.lower() + "." + t_fun.name + "(" + t_str + ")"
			self.codeValue += "\n\t\t\t" + t_fun.clas.name + "." + t_fun.clas.staticVar.name + "." + t_fun.name + "(" + t_str + ")"
		else:
			self.codeValue += "\n\t\t\t" + t_fun.name + "(" + t_str + ")"
	
	def StringValue(self):
		t_str = ""
		#用参数赋值参数
		if self.fun.isParameter:
			if RandomAS3.boolean():
				for item in self.fun.parameter:
					if item[1] == "String":
						if RandomAS3.boolean():
							t_str = item[0]
							return t_str
		
		#类变量赋值
		if len(self.clas.getVariable())>0:
			if RandomAS3.boolean():
				for item in self.clas.variables:
					if item.dataType == "String":
						if RandomAS3.boolean():
							t_str = item.name
							return t_str
		
		t_str = self.globalVaribleValue("String")
		if not t_str == "" and RandomAS3.boolean():
			return t_str
		
		t_str = self.randomStringValue()
		return t_str
	
	def IntValue(self):
		t_str = ""
		#用参数赋值参数
		if self.fun.isParameter:
			if RandomAS3.boolean():
				for item in self.fun.parameter:
					if item[1] == "int":
						if RandomAS3.boolean():
							t_str = item[0]
							return t_str
		
		#类变量赋值
		if len(self.clas.getVariable())>0:
			if RandomAS3.boolean():
				for item in self.clas.variables:
					if item.dataType == "int":
						if RandomAS3.boolean():
							t_str = item.name
							return t_str
		
		t_str = self.globalVaribleValue("int")
		if not t_str == "":
			return t_str
		
		t_str = str(random.randint(0,999999))
		return t_str
	
	def BoolValue(self):
		t_str = ""
		#用参数赋值参数
		if self.fun.isParameter:
			if RandomAS3.boolean():
				for item in self.fun.parameter:
					if item[1] == "Boolean":
						if RandomAS3.boolean():
							t_str = item[0]
							return t_str
		
		#类变量赋值
		if len(self.clas.getVariable())>0:
			if RandomAS3.boolean():
				for item in self.clas.variables:
					if item.dataType == "Boolean":
						if RandomAS3.boolean():
							t_str = item.name
							return t_str
		
		t_str = self.globalVaribleValue("Boolean")
		if not t_str == "":
			return t_str
		
		t_str = random.choice(['true','false'])
		return t_str
	
	def globalVaribleValue(self,t_dataType):
		t_str = ""
		#其他类变量赋值
		t_list = self.code.getVoid(t_dataType,self.clas.level)
		if len(t_list)>0:
			t_fun = random.choice(t_list)[0]
			
			if t_fun.isParameter:
				t_str = ""
				t_arr = t_fun.parameter
				for item in t_arr:
					t_list = self.clas.getVariableByType(item[1])
					if len(t_list)>0:
						t_str += random.choice(t_list)[1].name + ","
					else:
						t_list2 = self.code.getVariable(item[1],self.clas.level)
						if len(t_list2):
							t_class = random.choice(t_list2)
							# t_str += self.code.doc + "." + t_class[0][0].name.lower() + "." + t_class[0][1].name + ","
							t_str += t_class[0][0].name + "." + t_class[0][0].staticVar.name + "." + t_class[0][1].name + ","
						else:
							t_str += "new " + item[1] + "(),"
				
				t_str = t_str[0:-1]
				# t_str = self.code.doc + "." + t_fun.clas.name.lower() + "." + t_fun.name + "(" + t_str + ")"
				t_str = t_fun.clas.name + "." + t_fun.clas.staticVar.name + "." + t_fun.name + "(" + t_str + ")"
				return t_str
			else:
				return t_fun.clas.name + "." + t_fun.clas.staticVar.name + "." + t_fun.name + "()"
		return t_str
	
	def randomStringValue(self):
		#Xue
		t_str = ""
		num = random.randint(1,4)
		for i in range(num):
			t_str += str(random.randint(0,9))
		return "\"" + t_str + "\""


class AS3Function(object):
	DATA_TYPE = ["String", "int", "Boolean", "Class"]
	DATA_TYPE2 = ["String", "int", "Boolean"]
	
	def __init__(self, t_class, type, lv):
		self.clas = t_class
		self.code=t_class.code
		self.type = type
		self.level = lv
		self.name = randDict.getFun()
		self.returnNotVoid = RandomAS3.boolean()
		self.returnType = "void"
		self.returnType000 = self.returnType
		if self.returnNotVoid:
			self.returnType = random.choice(AS3Function.DATA_TYPE)
			if self.clas.level == 0:
				self.returnType = random.choice(AS3Function.DATA_TYPE2)
			self.returnType000 = self.returnType
			if self.returnType == "Class":
				self.returnType = self.code.getRandomClassUnderLevel(self.clas.level).name
		self.isParameter = RandomAS3.boolean()
		if self.isParameter:
			self.parameter = self.randomParameter()
		
		self.rows=None
	
	def createValue(self):
		#确定多少行代码
		t_row=random.randint(0,self.code.config['codeMax'])+1
		self.rows = []
		for idx in range(t_row):
			row=AS3CodeRow(self)
			row.initWithNotReturn()
			self.rows.append(row)
		
		if self.returnNotVoid:
			row=AS3CodeRow(self)
			row.initWithReturn()
			self.rows.append(row)
	
	def outParameter(self):
		if not self.isParameter:
			return ""
		t_str = ""
		for item in self.parameter:
			t_str += item[0] + ":" + item[1] + ", "
		return t_str[0:-1]
	
	def randomParameter(self):
		t_arr = []
		t_length = random.randint(1,3)
		for i in range(t_length):
			t_type = random.choice(AS3Function.DATA_TYPE)
			if self.clas.level == 0:
				t_type = random.choice(AS3Function.DATA_TYPE2)
			if t_type == "Class":
				t_type = self.code.getRandomClassUnderLevel(self.clas.level).name
			t_arr.append([randDict.getProto(), t_type])
		return t_arr
	
	def out(self):
		t_parameter = ""
		if self.isParameter:
			for item in self.parameter:
				t_parameter += item[0] + ": " + item[1] + ","
			t_parameter = t_parameter[0:-1]
		t_void = ":" + self.returnType
		
		t_rowStr = ""
		if len(self.rows)>0:
			for item in self.rows:
				t_rowStr += item.out() + "\n"
		
		t_str = "\t\t" + self.type + " function " + self.name + "(" + t_parameter + ")" + t_void + " {\n"
		t_str += t_rowStr
		t_str += "\t\t}\n"
		return t_str

	def isOpen(self):
		return self.type == AS3Class.PUBLIC
	
class AS3Variable(object):
	DATA_TYPE = ["String", "int", "Boolean"]
	
	def __init__(self,clas,type,t_static=False,t_name=None,t_dataType=None,t_initValue=False):
		self.value=None
		self.clas=clas
		self.code=clas.code
		self.type = type
		
		self.isStatic=t_static
		
		if t_name:
			self.name=t_name
		else:
			self.name = randDict.getProto()
	
		if t_dataType:
			self.dataType=t_dataType
		else:
			self.dataType = random.choice(AS3Variable.DATA_TYPE)
			if self.clas.level > 0 and random.random() > 0.7:
				self.dataType = "Class"
			if self.dataType == "Class":
				self.dataType = self.code.getRandomClassUnderLevel(self.clas.level).name
				
		if t_initValue:
			self.value=' = new '+t_dataType+'();'
		else:
			self.value=';'
		
	def out(self):
		type=self.type
		if self.isStatic:
			type+=' static'
		t_str = "\t\t" + type + " var " + self.name + ":" + self.dataType + self.value
		return t_str
	
	def isOpen(self):
		return self.type == AS3Class.PUBLIC


class AS3Class(object):
	PUBLIC="public"
	PRIVATE="private"
	TYPE = [PUBLIC, PRIVATE]
	
	def __init__(self,code,nm,pkg,lv):
		self.code=code
		self.name = nm
		self.package = pkg
		self.level = lv
		self.filePath=(self.package.replace('.', '\\') + '\\' + self.name + ".as").strip('\\')
		self.staticVar=None#自身类型的静态属性
		self.variables=None
		self.functions=None
		
		#----------------------------------------------------------------
		self.baseContent=None
		self.type=None#class or interface
		self.passInsert=0#跳过插入代码的几率，0表示每行后都插入代码，1表示完全不插入代码
	
	def createVariables(self,t_static=False):
		if t_static:
			self.staticVar=AS3Variable(self,AS3Class.PUBLIC,True,None,self.name,True)
		self.variables = []
		num = random.randint(0,self.code.config["varMax"]) + self.code.config["varMin"]
		for idx in range(num):
			t_obj = AS3Variable(self,AS3Class.PUBLIC)
			self.variables.append(t_obj)
			if RandomAS3.boolean():
				t_obj = AS3Variable(self,AS3Class.PRIVATE)
				self.variables.append(t_obj)
	
	def createFunctions(self):
		num = random.randint(0,self.code.config["funMax"]) + self.code.config["funMin"]
		levels = RandomAS3.rateArray(num, self.code.level_fun)#Xue
		self.functions = []
		for idx in range(num):
			t_obj = AS3Function(self, AS3Class.PUBLIC, levels.pop())
			self.functions.append(t_obj)
			if RandomAS3.boolean():
				t_obj = AS3Function(self, AS3Class.PRIVATE, random.randint(0,self.code.level_fun))
				self.functions.append(t_obj)
	
	def createFunctionsValue(self):
		for item in self.functions:
			item.createValue()
		
	
	def out(self):
		tStr = AS3Confuse.Template
		tStr = tStr.replace("{package}", self.package)
		tStr = tStr.replace("{import}", self.code.importstr)
		tStr = tStr.replace("{class}", self.name)
		tStr = tStr.replace("{variable}", self.outVariables())
		tStr = tStr.replace("{constructor}", "")
		tStr = tStr.replace("{function}", self.outFunctions())
		tStr = tStr.replace("{info}", "level:" + str(self.level))
		return tStr
		
	def outVariables(self):
		t_str = ""
		if self.staticVar:
			t_str += self.staticVar.out() + "\n"
		for item in self.variables:
			t_str += item.out() + "\n"
		return t_str
	
	def outFunctions(self):
		t_str = ""
		for item in self.functions:
			t_str += item.out() + "\n"
		return t_str
	
	def getVariable(self):
		t_arr=[]
		for item in self.variables:
			if item.isOpen():
				t_arr.append(item)
		return t_arr
	
	def getVariableByType(self,t_dataType):
		t_arr = []
		for item in self.variables:
			if item.isOpen() and item.dataType == t_dataType:
				t_arr.append([self, item])
		return t_arr
	
	def getFunc(self):
		t_arr=[]
		for item in self.functions:
			if item.isOpen():
				t_arr.append(item)
		return t_arr
	
	def getFuncPublicByParameter(self,t_ParameterType):
		t_arr=[]
		for item in self.functions:
			if item.isParameter and item.isOpen() and not item.returnNotVoid:
				for funArr in item.parameter:
					if funArr[1] == t_ParameterType:
						t_arr.append([self.name, item])
		return t_arr
	
	def getFuncPublicByNotVoid(self):
		t_arr = []
		for item in self.functions:
			if not item.returnNotVoid and item.isOpen():
				t_arr.append(item)
		return t_arr
	
	def getVoidByType(self,t_voidType):
		t_arr = []
		for item in self.functions:
			if item.returnNotVoid and item.isOpen() and item.returnType == t_voidType:
				t_arr.append(item)
		return t_arr
	
	def getFunctionsUnderLv(self,lv):
		arr=[]
		for item in self.functions:
			if item.level < lv:
				arr.append(item)
		return arr
	
	'''在代码行之间插入混淆代码'''
	def insertRandCode(self):
		if self.type=='interface':
			return
		#        元数据              包定义      import语句   switch语句  class语句       变量定义                    }   return      break      for
		regStrs=['\[\w+\((.*?)\)\]','package\\b','import\\b','switch\\b','public\s+class','([\w ]+?)?(var|const)\s','\}','return\\b','break\\b','for\\b']#匹配需要跳过插入代码的行
		#               写在单行的函数                     if       else
		regStrs.extend(['[\w ]*?\\bfunction\\b.*?\{.*?\}','if\\b','else\\b'])
		passLineReg=re.compile('|'.join(regStrs))
		staticReg=re.compile('\\b(static)?\s*(?:public|protected|private|internal)?\s+function\s+?((get|set)?\s*\w+)\s*\((.*?)\)\s*?(:\s*?\w+?)?\s*?\{')#匹配函数，如果是静态函数则跳过插入代码，直到遇到非静态函数再开始插入代码
		isStatic=False
		# ifelseReg=re.compile('')#匹配不带大括号的if else
		
		newLines=[]
		lines=self.baseContent.splitlines()
		while len(lines)>0:
			line=lines.pop(0)
			newLines.append(line)
			
			line=line.strip()
			
			m=staticReg.search(line)
			if m:
				if m.group(1)=='static':
					isStatic=True
				else:
					isStatic=False
			if isStatic:
				continue
			
			m=passLineReg.match(line)
			if not m:
				if RandomAS3.boolean(self.passInsert):
					num=random.randint(2,3)
					fun=EmptyFunction(self.code,self)
					for i in range(num):
						row=AS3CodeRow(fun)
						row.initWithNotReturn()
						fun.rows.append(row)
					newLines.append(AS3Confuse.markBlur(fun.out()))
			
		self.baseContent='\n'.join(newLines)
		print(u'插入代码完成：'+self.filePath)
		
	'''把生成的随机属性和方法加入到dependClass的class定义后'''
	def addRandCode(self):
		self.baseContent=self.code.clsReg.sub(self._outBaseSubFun,self.baseContent)
		print(u'添加代码完成：'+self.filePath)
	
	def _outBaseSubFun(self,m):
		gp=m.group()
		tp=m.group(1)
		if tp=='interface':
			return gp
		impt=AS3Confuse.markBlur(self.code.importstr)
		members=AS3Confuse.markBlur(self.outVariables()+'\n'+self.outFunctions())
		return impt+gp+members

class AS3Confuse(object):
	
	Template=None
	
	#添加表示混淆代码的注释
	@staticmethod
	def markBlur(cc):
		return '\n//-%-confuse-start-%-\n'+cc+'\n//-%-confuse-end-%-\n'
	
	def __init__(self):
		if not AS3Confuse.Template:
			AS3Confuse.Template=''\
'package {package}{//{info}\n\
	import flash.display.MovieClip;\n\
{import}\n\
	public class {class} extends MovieClip{\n\
{variable}\n\
		public function {class}() {\n\
{constructor}\n\
		}\n\
{function}\n\
	}\n\
}'
		self.config={"varMin": 5, "varMax": 10, "funMin": 5, "funMax": 10, "codeMax": 5}
		self.level_class=3
		self.level_fun=3
		
		self.doc_class=None
		self.doc_file=None
		self.doc=None
		
		self.numClass = 50
		self.pkglist=None
		self.importstr=None
		self.classList=None
		
		self.nativePath=None
		
		#------------------------------------------------------------------------------------------
		self.insertClsList=None
		self.passInsertGlobal=0
		self.passInsertDict={}
		
		self.noteReg=re.compile('\\/\\*(\\s|.)*?\\*\\/|(?<!:)\\/\\/.*')#注释
		self.braceReg=re.compile('(?<=\S)\s+\{')#大括号左半部分
		self.elseReg=re.compile('\}\s*else\\b')
		self.spaceReg=re.compile('(?<=\n)[ 	]*\n')#空行
		self.internalReg=re.compile('\\binternal\s+class\\b')#包内类:internal class
		# strReg=re.compile('".*?"|\'.*?\'')#字符串
		# reReg=re.compile('')#正则
		
		self.clsReg=re.compile('public\s+(class|interface)\s+(\w+)\s*(?:[\w\s,]+)?\{')#匹配public class类定义，添加import和属性，不包括包外类
		self.simpleClsReg=re.compile('\\b(class|interface)\s+(\w+)')
		
	def creat(self,t_path,t_num):
		self.formatFiles(t_path)
		self.createClass(t_num)
		self.insertCode(t_path)
		self.outFiles(t_path)
	
	'''格式化代码，检查代码格式'''
	def formatFiles(self,t_path):
		#classReg=re.compile('\bclass\b.*?\{')
		for root,dirs,files in os.walk(t_path):
			for file in files:
				fp=os.path.join(root,file)
				nm,ext=os.path.splitext(file)
				if ext=='.as':
					with open(fp) as f:
						cc=f.read()
					cc=self.noteReg.sub('',cc)
					cc=self.braceReg.sub('{',cc)
					cc=self.elseReg.sub('}else',cc)
					cc=cc.strip()#Xue  去掉文件开头和末尾的空字符
					cc=self.spaceReg.sub('',cc)
					cc=self.internalReg.sub('public class',cc)
					self.checkFormat(fp,cc)
					mh=self.clsReg.search(cc)
					if mh:
						if mh.group(2)!=nm:
							raw_input('file name not == class name')
					else:
						raw_input('not match class reg')
					
					with open(fp,'w') as f:
						f.write(cc)
						
	def checkFormat(self,fp,asfile):
		clsli=self.simpleClsReg.findall(asfile)
		if len(clsli)>=2:
			print(u'-->警告：不支持包内类定义，一个文件中只允许定义一个同名类。file:'+fp)
			raise Exception(fp)
	
	
	def insertCode(self,tpath):
		self.insertClsList=[]
		rootdir=os.getcwd()
		os.chdir(tpath)
		for root,dirs,files in os.walk('.'):
			pkg=root.replace('\\','.').strip('.')
			# print('pkg:'+pkg)
			for file in files:
				fp=os.path.join(root,file)
				nm,ext=os.path.splitext(file)
				if ext=='.as':
					asCls=AS3Class(self,nm,pkg,self.level_class)
					with open(fp) as f:
						asCls.baseContent=f.read()
					self.insertClsList.append(asCls)
					m=self.clsReg.search(asCls.baseContent)
					asCls.type=m.group(1)
					
		os.chdir(rootdir)
		for item in self.insertClsList:
			item.createVariables()
		for item in self.insertClsList:
			item.createFunctions()
		for item in self.insertClsList:
			item.createFunctionsValue()
		
		for item in self.insertClsList:
			item.passInsert=self.passInsertGlobal
			if item.name in self.passInsertDict:
				item.passInsert=self.passInsertDict[item.name]
			item.insertRandCode()
			
		for item in self.insertClsList:
			item.addRandCode()
		
		self.nativePath=tpath.replace('/','\\')
		for item in self.insertClsList:
			self.saveFile(item.filePath, item.baseContent)
	
	'''设置跳过插入代码的几率，0表示每行后都插入代码，1表示完全不插入代码，默认0'''
	def setGlobalInsertRate(self,rate):
		self.passInsertGlobal=rate
		
	'''设置特定类（文件）跳过插入代码的几率，0表示每行后都插入代码，1表示完全不插入代码，默认0'''
	def setInsertRate(self,name,rate):
		self.passInsertDict[name]=rate
	
	
	def createClass(self, t_num):
		self.numClass = t_num
		self.doc_class = randDict.getClass()
		self.doc_file = self.doc_class.replace('.', "/") + ".as"
		self.doc = self.doc_class.split('.')[-1]
		print(self.doc_class)
		
		#生成包，生成import
		self.pkglist = []
		self.importstr = ""
		numPkg = random.randint(3,5)
		numPkg = 1
		if numPkg > t_num:
			numPkg = t_num
		subPkg = randDict.getPkg()
		for i in range(numPkg):
			tPkg = "com." + subPkg + "." + randDict.getPkg()
			self.pkglist.append(tPkg)
			self.importstr += "\timport " + tPkg + ".*;\n"
		
			

		self.classList = []
		print(u"开始生成类...")
		
		self.updateCreateClass()
		self.updatecreateVariable()
		self.updatecreateFunctions()
		self.updatecreateFunctionsValue()
		
		# savePublicFun()
		
	
	#创建类
	def updateCreateClass(self):
		levels=RandomAS3.rateArray(self.numClass,self.level_class)
		for idx in range(self.numClass):
			self.classList.append(AS3Class(self, randDict.getClass(), self.pkglist[idx % len(self.pkglist)], levels.pop()))
			print(u"生成类: " + self.classList[idx].name + "\t" + str(idx + 1) + "/" + str(self.numClass))
		print(u"Class生成完成!")
	
	#创建变量
	def updatecreateVariable(self):
		for idx,item in enumerate(self.classList):
			item.createVariables(True)
			print(u"生成类变量: " + item.name + "\t" + str(idx + 1) + "/" + str(self.numClass))
		print(u"变量生成完成!")
	
	#创建方法
	def updatecreateFunctions(self):
		for idx,item in enumerate(self.classList):
			item.createFunctions()
			print(u"生成类方法: " + item.name + "\t" + str(idx + 1) + "/" + str(self.numClass))
	
	
	#创建方法内容
	def updatecreateFunctionsValue(self):
		for idx,item in enumerate(self.classList):
			item.createFunctionsValue()
			print(u"代码填充: " + item.name + "\t" + str(idx + 1) + "/" + str(self.numClass))
		
	def outFiles(self,root):
		self.nativePath=root.replace('/','\\')
		for idx,item in enumerate(self.classList):
			self.saveFile(item.filePath, item.out())
			print(u"生成代码文件: " + item.name + "\t" + str(idx + 1) + "/" + str(self.numClass))
		
		print(u"生成文档类")
		self.saveFile(self.doc_file, self.out())
		print(u"全部代码生成完成!")
	
	def saveFile(self, filePath, t_code):
		filePath=filePath.replace('/','\\')
		t_f=os.path.join(self.nativePath,filePath)
		targetParent=os.path.dirname(t_f)
		if not os.path.isdir(targetParent):
			os.makedirs(targetParent)
		with open(t_f,'w') as f:
			f.write(t_code)
	
	def savePublicFun(self):
		arr = self.getPulbicFuns()
		self.saveFile("rand_funs.txt", "\n".join(arr))
	
	def out(self):
		tVars = ""
		for idx,item in enumerate(self.classList):
			tVars += "\t\tpublic static var " + item.name.lower() + ":" + item.name + " = new " + item.name + "();\n"
		
		tArr = self.doc_class.split(".")
		del tArr[-1]
		tPkg = '.'.join(tArr)
		
		tStr = AS3Confuse.Template
		tStr = tStr.replace("{package}", tPkg)
		tStr = tStr.replace("{import}", self.importstr)
		tStr = tStr.replace("{class}", self.doc)
		tStr = tStr.replace("{variable}", tVars)
		tStr = tStr.replace("{constructor}", "")
		tStr = tStr.replace("{function}", "")
		return tStr
	
	def getVariable(self, t_dataType, lv):
		t_arr=[]
		for item in self.classList:
			if item.level<lv:
				t_list = item.getVariableByType(t_dataType)
				if len(t_list)>0:
					t_arr.append(t_list)
		return t_arr
	
	def getFuns(self, t_dataType, lv):
		t_arr=[]
		for item in self.classList:
			if item.level<lv:
				t_obj = item.getFuncPublicByParameter(t_dataType)
				if len(t_obj)>0:
					t_arr.append(t_obj)
		return t_arr
	
	def getFunsNotVoid(self, lv):
		t_arr=[]
		for idx,item in enumerate(self.classList):
			if item.level < lv:#Xue
				t_obj = item.getFuncPublicByNotVoid()
				if len(t_obj)>0:
					t_arr.append(t_obj)
		return t_arr
	
	def getVoid(self, t_voidType, lv):
		t_arr=[]
		for idx,item in enumerate(self.classList):
			if item.level < lv:#Xue
				t_obj = item.getVoidByType(t_voidType)
				if len(t_obj)>0:
					t_arr.append(t_obj)
		return t_arr
	
	def getRandomClass(self):
		return random.choice(self.classList)
	
	
	def getRandomClassByLevel(self, lv):
		classArr=[]
		for item in self.classList:
			if item.level == lv:
				classArr.append(item)
		if len(classArr)>0:
			return random.choice(classArr)
		else:
			return None
	
	
	def getRandomClassUnderLevel(self, lv):
		classArr=[]
		for item in self.classList:
			if item.level < lv:
				classArr.append(item)
		if len(classArr):
			return random.choice(classArr)
		else:
			return None
	
	
	def getPulbicFuns(self):
		def getFunParameters(type):
			resp = "null"
			if type == "int": 
				resp = str(random.randint(0,9999))
			elif type == "Boolean": 
				resp = "true"
			elif type == "String": 
				resp = '"' + str(random.randint(0,9999)) + '"'
			return resp
		
		arr = []
		for item in self.classList:
			for fun in item.functions:
				if fun.type == "public":
					if fun.parameter:
						paras = []
						tArr = fun.parameter.concat()
						while len(tArr)>0:
							paras.append(getFunParameters(tArr.shift()[1]))
						arr.append(self.doc + "." + item.name.lower() + "." + fun.name + "(" + ", ".join(paras) + ");")
					else:
						arr.append(self.doc + "." + item.name.lower() + "." + fun.name + "();")
		
		return arr

if __name__=='__main__':
	src='rand/src'
	if os.path.isdir(src):
		shutil.rmtree(src)
	shutil.copytree('D:\h5pkg\develop\src',src)
	
	ac=AS3Confuse()
	ac.formatFiles(src)
	ac.createClass(20)
	ac.insertCode(src)
	ac.outFiles(src)















