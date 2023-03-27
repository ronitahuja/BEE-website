from flask import Flask,render_template,request,url_for,redirect,session,jsonify
from pymongo import MongoClient
import csv
from datetime import datetime
import json
# with open('contact.csv','w',newline="") as file:
#     myfile=csv.writer(file)
with open('personal projects/bee website/templates/config.json','r') as c:
    params=json.load(c)["params"]
app=Flask(__name__)
client = MongoClient(params['mongoclient'])
db = client['bee_website_database']
contact_collection=db['bee-contact']

@app.route("/")
def home():
    return render_template("index.html",params=params)

@app.route('/kvl')
def kvl():
    return render_template("kvl.html",params=params)

@app.route('/kcl')
def kcl():
    return render_template("kcl.html",params=params)

@app.route('/about')
def about():
    return render_template("about.html",params=params)

@app.route('/contact',methods=['POST','GET'])
def contact():
    if request.method=='POST':
        now=datetime.now()
        with open('personal projects/bee website/templates/contact.csv','a',newline="") as file:
            myfile=csv.writer(file)
            # myfile.writerow(["name","branch","email","message"])
            myfile.writerow({request.form.get('contactname'),
                            request.form.get('contactmsg')
                                    })
        # contact_collection.insert_one({'name':request.form.get('contactname'),
        #                                 'enrollment number':request.form.get('rollno'),
        #                                 'branch':request.form.get('branch').upper(),
        #                                 'section':request.form.get('sec').upper(),
        #                                 'email':request.form.get('contactemail'),
        #                                 'phone number':request.form.get('contactphone'),
        #                                 'message':request.form.get('contactmsg'),
        #                                 'date and time':now.strftime("%d-%m-%y \n %H:%M:%S")})
    return render_template("contact.html",params=params)

@app.route("/database",methods=['post','get'])
def databaselogin():
    if request.method=="POST":
        user=request.form.get("loginname")
        mail=request.form["loginemail"]
        password=request.form.get("loginpassword")
        finduser=params['contact_username']
        if user==finduser:
            if params['contact_password']==password and params['contact_email']==mail:
                contact_records=db.get_collection("bee-contact").find({},{'_id':0})
                return render_template("contact_records.html",params=params,contacts=contact_records)
            else:
                return "invalid credentials"
        else:
            return "not a user"
    return render_template("databaselogin.html")

@app.route("/virtuallab")
def virtuallab():
    return render_template("virtuallab.html",params=params)

if __name__=='__main__':
    app.run(debug=False,host='0.0.0.0')