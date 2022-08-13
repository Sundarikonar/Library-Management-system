from email import message
from flask import Flask,render_template,request,redirect,url_for
import pymysql
db_connection=None
tb_cursor=None

app=Flask(__name__)

def connecttodb():
    global db_connection
    global tb_cursor
    db_connection=pymysql.connect(user="root",password="",host="localhost",database="library",port=3306)
    if (db_connection):
        print("Connected!")
        tb_cursor=db_connection.cursor()
    else:
        print("Error!!")

def getalldata():
    connecttodb()
    select_query="select * from books"
    tb_cursor.execute(select_query)
    alldata=tb_cursor.fetchall()
    disconnectdb()
    print(alldata)
    return alldata

def insertintobooks(bookname,author,issuedby,issuedate,charges):
    connecttodb()
    insertdata="insert into books(bookname,author,issuedby,issuedate,charges) Values(%s,%s,%s,%s,%s);"
    tb_cursor.execute(insertdata,(bookname,author,issuedby,issuedate,charges))
    db_connection.commit()
    disconnectdb()
    return True

def getbookid(id):
    connecttodb()
    selectquery="SELECT * from books where id=%s;"
    tb_cursor.execute(selectquery,(id,))
    onedata=tb_cursor.fetchone()
    disconnectdb()
    return onedata

def updateintotable(bookname,author,issuedby,issuedate,charges,id):
    connecttodb()
    updatequery="UPDATE books set bookname=%s,author=%s,issuedby=%s,issuedate=%s,charges=%s where id=%s"
    tb_cursor.execute(updatequery,(bookname,author,issuedby,issuedate,charges,id))
    db_connection.commit()
    disconnectdb()
    return True

def deletebooksfromtable(id):
    connecttodb()
    deletequery="DELETE FROM books WHERE id=%s"
    tb_cursor.execute(deletequery,(id,))
    db_connection.commit()
    disconnectdb()
    return True

def disconnectdb():
    db_connection.close()
    tb_cursor.close()

@app.route("/")
def index():
    alldata=getalldata()
    return render_template("index.html",data=alldata)

@app.route("/add",methods=["GET","POST"]) 
def addbooks():
    if request.method=="POST":
        data=request.form
        isinserted=insertintobooks(data["txtName"],data["txtauthor"],data["txtissuedby"],data["txtdoi"],data["numbercharge"])
        if(isinserted):
            message="Inserted succesfully!!"
        else:
            message="Error in insertion"
        return render_template("add.html",message=message)
    return render_template("add.html")

@app.route("/update/",methods=["GET","POST"])
def updatebooks():
    id=request.args.get("ID",type=int,default=1)
    idData=getbookid(id)
    if request.method=="POST":
        data=request.form
        isupdated=updateintotable(data["txtName"],data["txtauthor"],data["txtissuedby"],data["txtdoi"],data["numbercharge"],id)
        if(isupdated):
            message="Updated succesfully!!"
        else:
            message="Error in Updation"
        return render_template("update.html",message=message)
    return render_template("update.html",data=idData)

@app.route("/delete/")
def deletebooks():
    id=request.args.get("ID",type=int,default=1)
    deletebooksfromtable(id)
    return redirect(url_for("index"))

if __name__=="__main__":
    app.run(debug=True)

