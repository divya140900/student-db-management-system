'''PYTHON INTERNSHIP PROJECT :--
		STUDENT MANAGEMENT SYSTEM (GUI, PDBC + Data Science)'''


from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import socket
import requests
import bs4
import matplotlib.pyplot as plt
import pandas as pd


root = Tk()

#function to get location

def f1():
	try:
		socket.create_connection(("www.google.com",80))
		res=requests.get("https://ipinfo.io")
		data=res.json()
		city_name=data['city']
		return city_name
	except OSError as e:
		print("issue ",e)

#function to get temperature

def f2():
	try:
		socket.create_connection( ("www.google.com", 80))
		city = f1()
		a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
		a2 = "&q=" + city 
		a3 = "&appid=c6e315d09197cec231495138183954bd"
		api_address =  a1 + a2  + a3 		
		res = requests.get(api_address)
		data=res.json()
		main=data['main']
		temp1=str(main['temp'])
		return temp1
	except OSError as e:
		print("issue ", e)

#function to get QOTD

def f3():
	try:
		socket.create_connection(("www.google.com",80))	
		res=requests.get("https://www.brainyquote.com/quote_of_the_day")
		soup=bs4.BeautifulSoup(res.text,"lxml")
		data=soup.find("img",{"class":"p-qotd"})
		msg=data['alt']
		return msg
	except Exception as e:
		print("issue ",e)

#Validations

def validation_r(inp):
	if inp.isdigit() or inp is "":
		print(inp)
		return True
	else:
		print(inp) 
		showerror("check","Enter a valid number.")
		return False

def validation_n(inp):
	if all(char.isalpha() or char.isspace() for char in inp):
		print(inp)
		return True
	elif inp is "":
		return True
	else:
		print(inp)
		return False
	
	
def f4():
	addrno.delete(0,END)
	addname.delete(0,END)
	addmarks.delete(0,END)
	adst.deiconify()
	root.withdraw()

#to view the data

def f5():
	stdata.delete(1.0,END)
	vist.deiconify()
	root.withdraw()
	con=None
	try:
		con=connect("St_record.db")
		print("connected")
		cursor=con.cursor()  
		sql="select * from entries"  
		cursor.execute(sql)   
		data=cursor.fetchall()
		info=""
		for d in data:
			info=info+"Rno: "+str(d[0])+"  Name: "+str(d[1])+"  Marks: "+str(d[2])+"\n"
		stdata.insert(INSERT,info)
	except Exception as e:
		showerror("check",("issue "+e))
		con.rollback()
	finally:
		if con is not None:
			con.close()
			print("disconnected")

def f6():
	addUrno.delete(0,END)
	addUname.delete(0,END)
	addUmarks.delete(0,END)
	upst.deiconify()
	root.withdraw()

def f7():
	addDrno.delete(0,END)
	dest.deiconify()
	root.withdraw()

def f8():
	root.deiconify()
	adst.withdraw()

def f9():
	root.deiconify()
	vist.withdraw()

def f10():
	root.deiconify()
	upst.withdraw()

def f11():
	root.deiconify()
	dest.withdraw()

#to insert data

def f12():
	con=None
	try:
		con=connect("St_record.db")
		print("connected")
		rno=int(addrno.get())
		name=addname.get()
		marks=int(addmarks.get())
		if len(name)<2:
			showerror("check","Enter a valid name.")
		elif marks<0 or marks>100:
			showerror("check","enter valid marks.")
		else:
			args=(rno,name,marks)
			cursor=con.cursor()   
			sql="insert into entries values('%d','%s','%d')"  
			cursor.execute(sql % args)  
			con.commit()
			showinfo("success","record added")
	except Exception as e:
		showerror("issue ",e)
		con.rollback()
	finally:
		if con is not None:
			con.close()
			print("disconnected")

#to update data

def f13():
	class MyException(Exception):
		def __init__(self,msg):
			self.msg=msg
	con=None
	try:	
		
		con=connect("St_record.db")
		cursor=con.cursor() 
		print("connected")
		Rno=int(addUrno.get())
		sql="select * from entries where rno='%d';"
		args=(Rno)
		cursor.execute(sql %args)
		data=cursor.fetchone()
		if data==None:
			raise MyException("record does not exists")
		prv_name=data[1]
		prv_marks=data[2]
		if addUname.get()!="":
			name=addUname.get()
		else:
			name=prv_name
		if addUmarks.get()!="":
			marks=int(addUmarks.get())
		else:
			marks=prv_marks
		if len(name)<2:
			showerror("check","Enter a valid name.")
		elif marks<0 or marks>100:
			showerror("check","enter valid marks.")
		else:
			args=(marks,name,Rno)
			sql="update entries set marks = '%d',name = '%s' where rno= '%d'"  
			cursor.execute(sql % args)   
			con.commit()
			showinfo("success","record updated")
	except Exception as e:
		showerror("failure"," update issue "+str(e))
		con.rollback()
	finally:
		if con is not None:
			con.close()
			print("disconnected")

#to delete data

def f14():
	con=None
	try:
		con=connect("St_record.db")
		print("connected")
		rno=int(addDrno.get())
		args=(rno)
		cursor=con.cursor() 
		sql="delete from entries where rno='%d'"  
		cursor.execute(sql % args)   
		if cursor.rowcount>=1:
			con.commit()
			showinfo("success","record deleted")
		else:
			showinfo("check","record does not exists")
	except Exception as e:
		showerror("failure"," delete issue "+str(e))
		con.rollback()
	finally:
		if con is not None:
			con.close()
			print("disconnected")

#to plot bar graph

def f15():
	con=None
	try:
		con=connect("St_record.db")
		print("connected")
		cursor=con.cursor()  
		data1=pd.read_sql_query("select * from entries order by marks DESC LIMIT 5 ",con)  
		st_names=data1['name'].tolist()
		st_marks=data1['marks'].tolist()
		colors='rgbyk'
		plt.bar(st_names,st_marks,width=0.3,color=colors)
		plt.xlabel("names")
		plt.ylabel("marks")
		plt.title("Batch information!")
		plt.show()
	except Exception as e:
		showerror("failure"," issue "+str(e))
		con.rollback()
	finally:
		if con is not None:
			con.close()
			print("disconnected")
	
#design of root window  ---> student management system

root.title("S.M.S")
root.geometry("500x600+400+100")
root.resizable(0, 0)
root.configure(background = "light green")

btnadd=Button(root, text = "Add", font = ("arial", 18, "bold"),width = 15,command=f4)
btnview=Button(root, text = "View", font = ("arial", 18, "bold"),width = 15,command=f5)
btnupdate=Button(root, text = "Update", font = ("arial", 18, "bold"),width = 15,command=f6)
btndelete=Button(root, text = "Delete", font = ("arial", 18, "bold"),width = 15,command=f7)
btnchart=Button(root, text = "Chart", font = ("arial", 18, "bold"),width = 15,command=f15)
labellocation=Label(root, text = ("Location : "+f1()),font = ("arial", 18),background="light green")
labeltemp=Label(root, text="Temp : "+f2(),font = ("arial", 18),background="light green")
labelqotd=Label(root, text="QOTD :",font = ("arial", 16, "bold"),background="light green")
labelquote=Label(root,text=f3(),justify = LEFT,wraplength = 300,font = ("arial", 14 , "bold"),background="light green")

btnadd.pack(pady = 10)
btnview.pack(pady = 10)
btnupdate.pack(pady = 10)
btndelete.pack(pady = 10)
btnchart.pack(pady = 10)
labellocation.place(x=30,y=400)
labeltemp.place(x=325,y=400)
labelqotd.place(x=30,y=475)
labelquote.place(x=125,y=475)

#design of Add st ---> add student

adst = Toplevel(root)
adst.title("Add St.")
adst.geometry("500x600+400+100")
adst.resizable(0, 0)
adst.withdraw()
adst.configure(background = "light blue")

labelentrno=Label(adst, text="Enter rno:",font = ("arial", 18, "bold"),background="light blue") 
addrno=Entry(adst , bd=15, font = ("arial", 18, "bold"),width=20)
labelentrno.pack(pady=10)
addrno.pack(pady=10)
addrno.focus() 
reg1 = adst.register(validation_r)
addrno.config(validate="key",validatecommand=(reg1,'%P'))

labelentname=Label(adst, text="Enter name:",font = ("arial", 18, "bold"),background="light blue")
addname=Entry(adst , bd=15, font = ("arial", 18, "bold"),width=20)
labelentname.pack(pady=15)
addname.pack(pady=10)
reg2 = adst.register(validation_n)
addname.config(validate="key",validatecommand=(reg2,'%P'))

labelentmarks=Label(adst, text="Enter marks:",font = ("arial", 18, "bold"),background="light blue")
addmarks=Entry(adst , bd=15, font = ("arial", 18, "bold"),width=20)
labelentmarks.pack(pady=10)
addmarks.pack(pady=10)

btnsave=Button(adst, text = "Save", font = ("arial", 18, "bold"),width=15,command=f12)
btnsave.pack(pady=25)

btnback=Button(adst, text = "Back", font = ("arial", 18, "bold"),width=15,command=f8)
btnback.pack(pady=10)

#design of vist ---> view student

vist=Toplevel(root)
vist.title("View St.")
vist.geometry("500x600+400+100")
vist.resizable(0, 0)
vist.withdraw()
vist.configure(background = "LightGoldenrod1")

stdata=ScrolledText(vist, width="40", height="30")
btnbackv=Button(vist, text = "Back", font = ("arial", 18, "bold"),width=15,command=f9)

stdata.pack(pady=10)
btnbackv.pack(pady=10)

#design of upst ---> update student

upst=Toplevel(root)
upst.title("Update St.")
upst.geometry("500x600+400+100")
upst.resizable(0, 0)
upst.withdraw()
upst.configure(background = "light pink")

labelentUrno=Label(upst, text="Enter rno:",font = ("arial", 18, "bold"),background="light pink")
addUrno=Entry(upst , bd=15, font = ("arial", 18, "bold"),width=20)
labelentUrno.pack(pady=10)
addUrno.pack(pady=10)
addUrno.focus()
reg4 = upst.register(validation_r)
addUrno.config(validate="key",validatecommand=(reg4,'%P'))

labelentUname=Label(upst, text="Enter name:",font = ("arial", 18, "bold"),background="light pink")
addUname=Entry(upst , bd=15, font = ("arial", 18, "bold"),width=20)
labelentUname.pack(pady=10)
addUname.pack(pady=10)
reg5 = upst.register(validation_n)
addUname.config(validate="key",validatecommand=(reg5,'%P'))

labelentUmarks=Label(upst, text="Enter marks:",font = ("arial", 18, "bold"),background="light pink")
addUmarks=Entry(upst , bd=15, font = ("arial", 18, "bold"),width=20)
labelentUmarks.pack(pady=10)
addUmarks.pack(pady=10)

btnsaveu=Button(upst, text = "Save", font = ("arial", 18, "bold"),width=15,command=f13)
btnsaveu.pack(pady=25)
btnbacku=Button(upst, text = "Back", font = ("arial", 18, "bold"),width=15,command=f10)
btnbacku.pack(pady=10)

#design of dest --->delete student

dest=Toplevel(root)
dest.title("Delete St.")
dest.geometry("500x600+400+100")
dest.resizable(0, 0)
dest.withdraw()
dest.configure(background = "SeaGreen1")

labelentDrno=Label(dest, text="Enter rno:",font = ("arial", 18, "bold"),background="SeaGreen1")
addDrno=Entry(dest , bd=15, font = ("arial", 18, "bold"),width=20)
labelentDrno.pack(pady=15)
addDrno.pack(pady=15)
addDrno.focus()
reg3 = dest.register(validation_r)
addDrno.config(validate="key",validatecommand=(reg3,'%P'))

btnsaved=Button(dest, text = "Save", font = ("arial", 18, "bold"),width=15,command=f14)
btnsaved.pack(pady=25)

btnbackd=Button(dest, text = "Back", font = ("arial", 18, "bold"),width=15,command=f11)
btnbackd.pack(pady=15)

root.mainloop()
