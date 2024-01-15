from flask import Flask, render_template,request,redirect,url_for,flash;
# from flask_sqlalchemy import SQLAlchemy;
import smtplib
import random
from twilio.rest import Client
import re
import pymongo
from pymongo import MongoClient
import string
import secrets
import datetime
import csv
import requests
import json
from flask_mail import Mail, Message
from flask_mail import Connection

from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication



app = Flask(__name__)
client = MongoClient('localhost', 27017)
app.secret_key ="Secret Key"
app.config['MAIL_SERVER'] ='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'prasoonyash@gmail.com'
app.config["MAIL_PASSWORD"] = ''
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
# msg = Message(app)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/ac'
# app.config['SQLALCHEMY_TRACK_MODIFICARTIONS']=False
db = client.acc_open
account_open = db.account_open
account_data = db.account_data
data_customer = db.data_customer

phone_otp = 0
email_otp = 0

status = True
name = ""
f_name =""
m_name = ""
dob ="" 
aadhar = ""
pan =  ""
email= ""
phone = ""
type_ac =""
nominee =""
occupation=""
address =""
photo_upload =""
sign_upload =""
server =""

a_no =""
password =""
secret_key =""

session_account_number =""

# # db = SQLAlchemy(app)
# class Acc(db.Model):
#     # id = db.Column(db.Integer, primary_key = True)
#     name = db.Column(db.String(1000),primary_key = True)
#     email =db.Column(db.String(1000))
#     comment = db.Column(db.String(1000))


#     def __init__(self,name,email,comment):
#         self.name = name
#         self.email = email
#         self.comment = comment
def email_alert(subject, body, email,name):
    # message = EmailMessage()
    # message.set_content(body)
    # message['subject'] = subject
    # message['to'] = to
    # message['']

    # user = "prasoonyash@gmail.com"
    # message['from']= user
    # password = ''

    # server.smtplib.SMTP("smtp.gmail.com",587)
    # server.starttls()
    # server.login(user,password)
    # server.send_message(message)
    # server.quit()

    # #######################
    sender_email = "prasoonyash@email.com"
    receiver_email = email

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    msgText = MIMEText('<b>%s</b>' % (body), 'html')
    msg.attach(msgText)

    # filename = "example.txt"
    # msg.attach(MIMEText(open(filename).read()))

    # with open('example.jpg', 'rb') as fp:
    #     img = MIMEImage(fp.read())
    #     img.add_header('Content-Disposition', 'attachment', filename="example.jpg")
    #     msg.attach(img)
        
    pdf = MIMEApplication(open("example.pdf", 'rb').read())
    pdf.add_header('Content-Disposition', 'attachment', filename= f"{name}.csv")
    msg.attach(pdf)

    try:
        with smtplib.SMTP('smtp.office365.com', 587) as smtpObj:
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login("prasoonyash@gmail.com", "")
            smtpObj.sendmail(f"{email}", receiver_email, msg.as_string())
    except Exception as e:
        return e

def valid_dob():

    return True

def valid_pan(pan):
    result = re.compile("[A-Za-z]{5}\d{4}[A-Za-z]{1}")
    return result.match(pan)

def valid_phone(number):
    if(len(number)==10 and number.isdigit()):
        return True
    else:
        return False
    
def valid_email(email):
    if re.match(r'[^@]+@[^@]+\.[^@}]+',email):
        return True
    else:
        return False
    
def valid_aadhar(aadhar):
    if(len(aadhar)==12 and aadhar.isdigit()):
        return True
    else:
        return False
    
def valid_name(name):
    regex_name = re.compile(r'([a-z]+)( [a-z]+)*( [a-z]+)*$',re.IGNORECASE)
    res = regex_name.search(name)
    return res

@app.route('/sign_up')
def sign_up():
    return render_template('account_opening.html')

@app.route('/', methods=('GET', 'POST'))
def home():
    return render_template('home.html')

@app.route('/valid',methods=('GET','POST'))
def valid():
    if request.method=='POST':
        global a_no
        global password
        global secret_key
        customer_email_otp =request.form['customer_email_otp']
        customer_phone_otp =request.form['customer_phone_otp']
        # print(customer_email_otp)
        # print(customer_phone_otp)
        # print(phone_otp)
        # print(email_otp)
        # print(type(customer_email_otp))
        # print(type(customer_phone_otp))
        # print(type(phone_otp))
        # print(type(email_otp))
        
        if(customer_phone_otp ==str(phone_otp) and customer_email_otp == str(email_otp)):
            now = datetime.datetime.now()
            account_open.insert_one({'datetime':now,'name':name,'f_name':f_name,'m_name':m_name,'dob':dob,'aadhar':aadhar,'pan':pan,'email':email,'phone':phone,'type_ac':type_ac,'nominee':nominee,'occupation':occupation,'address':address,'photo_upload':photo_upload,'sign_upload':sign_upload})
            a_no =random.randint(10000000000000,99999999999999)
            secret_key =random.randint(1000,9999)
            letters = string.ascii_letters
            digits = string.digits
            special_chars = string.punctuation
            alphabet = letters + digits + special_chars
            pwd_length = 12
            for i in range(pwd_length):
                # print("a")
                password += ''.join(secrets.choice(alphabet))
            message = f"Welcome to Lakshmi Bank.\n\nॐ भोगलक्ष्म्यै नम: ||\nॐ योगलक्ष्म्यै नम: ||\n\nHi Lakshmi member,\nYour account has been successfully created \n\nAccount no :- {a_no}\nIFSC Code :- LKSB678987\nYour password :- {password}\nYour secret key :- {secret_key}\n\nPlease save your password and secret key ,these will be used during signin.\n\nDONOT SHARE YOUR CREDENTIALS  WITH ANYONE".encode("utf-8")
            
            # email_alert("Account Opening",message,email,name,)
            status = True
            with smtplib.SMTP_SSL("smtp.gmail.com",465) as server:
                print("9999")
                server.login('prasoonyash@gmail.com','')
                server.sendmail('prasoonyash@gmail.com',email,message)
            print("8888")
            account_data.insert_one({'datetime':now,'a_no':a_no, 'password':password,'secret_key':secret_key,'name':name,'f_name':f_name,'m_name':m_name,'dob':dob,'aadhar':aadhar,'pan':pan,'email':email,'phone':phone,'type_ac':type_ac,'nominee':nominee,'occupation':occupation,'address':address,'photo_upload':photo_upload,'sign_upload':sign_upload})
            data_customer.insert_one({'a_no':a_no,'balance':0})
            cursor =account_data.find_one({'a_no':a_no})
            with open(f"{cursor['name']}.csv", 'a', newline='') as file:
                writer = csv.writer(file)
                
                field = ["a_no","amount","net_balance"]
                writer.writerow(field)
            with open('account_data.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                
                field = ["datetime","account_number","password","secret_key","name","father name","mother name","DOB","aadhar","pan","email","phone","type_ac","nominee","occupation","address"]
                
                writer.writerow(field)
                writer.writerow([f"{now}",f"{a_no}",f"{password}",f"{secret_key}",f"{name}",f"{f_name}",f"{m_name}",f"{dob}",f"{aadhar}",f"{pan}",f"{email}",f"{phone}",f"{type_ac}",f"{nominee}",f"{occupation}",f"{address}"])
                
            

            
        else:
            flash("Please provide correct credentials")
        return render_template('success.html')

@app.route('/oops')
def oops():
    return render_template('oops.html')

@app.route('/insert',methods =["POST"])
def insert():
    if request.method =='POST':
        global name
        global f_name
        global m_name
        global dob
        global aadhar
        global pan
        global email
        global phone
        global type_ac
        global nominee
        global occupation
        global address
        global photo_upload
        global sign_upload
        global status
        name = request.form['name']
        f_name = request.form['f_name']
        m_name = request.form['m_name']
        dob = request.form['dob']
        aadhar = request.form['aadhar']
        pan =  request.form['pan']
        email = request.form['email']
        phone = request.form['phone']
        type_ac = request.form['type_ac']
        nominee = request.form['nominee']
        occupation = request.form['occupation']
        address = request.form['address']
        photo_upload = request.form['photo_upload']
        sign_upload = request.form['sign_upload']
        status = True
        # print(f'a{status}')
        if(not (valid_name(name) and valid_name(f_name) and valid_name(m_name))):
            flash ("Please check ypour name")
            status = False
            # print(f'b{status}')
            # return redirect(url_for('home'))
        
        if(not(valid_dob())):
            flash("Please enter valid dob")
            status = False
            # print(f'c{status}')

            # return redirect(url_for('home'))
            pass


        if(not valid_aadhar(aadhar)):
            flash("Please enter valid aadhar")
            status = False
            # print(f'd{status}')
            # return redirect(url_for('home'))

        if(not valid_pan(pan)):
            flash("Please enter valid pan")
            status = False
            # print(f'e{status}')
            # return redirect(url_for('home'))

        if(valid_email(email)):
            global email_otp
            email_otp = random.randint(100000,999999)
            message = f"Hi {name},\n Your email OTP verification code is {email_otp} "
            with smtplib.SMTP_SSL("smtp.gmail.com",465) as server:
                server.login('prasoonyash@gmail.com','')
                server.sendmail('prasoonyash@gmail.com',email,message)
        else:
            flash("Please enter valid email address")
            status = False
            # print(f'f{status}')
            


        if(valid_phone(phone)):

            global phone_otp
            phone_otp = random.randint(100000,999999)
            # url ="https://www.fast2sms.com/dev/bulk"
            # my_data = {'sender_id':'FTWSMS', 'meassage': f'Your mobile verification OTP is {phone_otp}','language':'english','route':'V3','numbers':f'{phone}','flash' :'0'}
            # headers = {
            #             'authorization': 'ekvyNxCUtcT59WFwBiaM0ZjG14qgkP7lwBq3VixSetgabNMfJ1dnArF9',
            #             'Content-Type': "application/x-www-form-urlencoded",
            #             'Cache-Control': "no-cache"
            #         }
            # response = requests.request("POST",url,data = my_data,headers = headers)
            
            account_sid = 'AC9968264f236a0b63b1f569'
            auth_token ='18d7bf748dc9bccf4c8'
            client = Client(account_sid,auth_token)
    
            msg = client.messages.create(body =f"Your mobie OTP verification code  is {phone_otp}",from_ ="+1315873",to = f"+91{phone}")

        else:
            flash("Please enter a valid phone number")
            status = False
            # print(f'g{status}')
            # return redirect(url_for('home'))

        

        if(status):return render_template('validation.html')
        else:
            # print(f'h{status}')
            return redirect(url_for('oops'))



# for login of existing customers
@app.route('/signin_validation',methods=['POST'])
def signin_validation():
    global session_account_number
    global a_no
    global password
    global secret_key
    a_no = int(request.form['a_no'])
    password = request.form['password']
    secret_key = request.form['secret_key']
    session_account_number = a_no
    # print(type(a_no))
    # print(type(password))
    # print(type(secret_key))

    document = account_data.find_one({'a_no':a_no})
    # print(type(document['a_no']))
    # print(type(document['password']))
    # print(type(document['secret_key']))
    # print(document)
    if(str(document['a_no'])== str(a_no) and str(document['password'])== password and str(document['secret_key'])== secret_key):
        message = f"Hi {str(document['name'])},\nYou have successfully login to your account."
        with smtplib.SMTP_SSL("smtp.gmail.com",465) as server:
                server.login('prasoonyash@gmail.com','')
                server.sendmail('prasoonyash@gmail.com',str(document['email']),message)
        name = document['name']
        return render_template('services.html',name = name)
    else:
        return(redirect(url_for('oops')))


@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/transfer')
def transfer():
    return render_template('transfer_customer.html')

@app.route('/transfer_customer',methods=['POST'])
def transfer_customer():
    sender_account = int(request.form['sender_account'])
    receiver_account = int(request.form['receiver_account'])
    amount_send = int(request.form['amount_send'])
    sender =data_customer.find_one({'a_no':sender_account})
    receiver = data_customer.find_one({'a_no': receiver_account})
    # print(receiver['balance'])
    # print(sender['balance'])
    amount_receiver = int(receiver['balance'])
    amount_sender = int(sender['balance'])
    
    if(int(sender['balance']>amount_send)):
        data_customer.update_one({'a_no':receiver_account},{ "$set": { "balance": amount_receiver+amount_send }})
        data_customer.update_one({'a_no':sender_account},{ "$set": { "balance": amount_sender-amount_send }})
        sender =data_customer.find_one({'a_no':sender_account})
        receiver = data_customer.find_one({'a_no': receiver_account})
    

        verify_receiver = account_data.find_one({'a_no':receiver_account})
        verify_sender = account_data.find_one({'a_no':sender_account})

        message = f"Hi {str(verify_receiver['name'])},\nYour account has been credited Rs {amount_send}\nYour current balance is {str(receiver['balance'])} "
        with smtplib.SMTP_SSL("smtp.gmail.com",465) as server:
                server.login('prasoonyash@gmail.com','')
                server.sendmail('prasoonyash@gmail.com',str(verify_receiver['email']),message)
        message = f"Hi {str(verify_sender['name'])},\nYour account has been debited Rs {amount_send}.\nYour current balance is {str(sender['balance'])}"
        with smtplib.SMTP_SSL("smtp.gmail.com",465) as server:
                server.login('prasoonyash@gmail.com','')
                server.sendmail('prasoonyash@gmail.com',str(verify_sender['email']),message)
        with open(f"{verify_receiver['name']}.csv", 'a', newline='') as file:
            writer = csv.writer(file)
                
            field = [f"Trasfered by {sender_account}",f"{amount_send}",f"{str(receiver['balance'])}"]
            writer.writerow(field)
        with open(f"{verify_sender['name']}.csv", 'a', newline='') as file:
            writer = csv.writer(file)
                
            field = [f"Trasfered to {sender_account}",f"{amount_send}",f"{str(sender['balance'])}"]
            writer.writerow(field)
        return render_template('success.html')


@app.route('/deposit')
def deposit():
    return render_template('deposit_customer.html')

@app.route('/deposit_customer',methods=['POST'])
def deposit_customer():
    depositor_account_number = int(request.form['depositor_account_number'])
    deposit_amount = int(request.form['deposit_amount'])

    deposit_details = data_customer.find_one({'a_no':depositor_account_number})
    balance = int(deposit_details['balance'])
    data_customer.update_one({'a_no':depositor_account_number},{ "$set": { "balance": balance+deposit_amount }})
    deposit_details = data_customer.find_one({'a_no':depositor_account_number})
    # deposit_details['balance']= balance+deposit_amount
    print(balance)
    print(deposit_amount)
    print(deposit_details['balance'])
    depositor_details = account_data.find_one({'a_no':depositor_account_number})
    # print((depositor_details['name']))

    message = f"Hi {str(depositor_details['name'])},\nYour account has been deposited Rs {deposit_amount}\nYour current balance is {str(deposit_details['balance'])}"
    with smtplib.SMTP_SSL("smtp.gmail.com",465) as server:
        server.login('prasoonyash@gmail.com','')
        server.sendmail('prasoonyash@gmail.com',str(depositor_details['email']),message)
    with open(f"{depositor_details['name']}.csv", 'a', newline='') as file:
        writer = csv.writer(file)
                
        field = [f"Deposited by {depositor_account_number}",f"{deposit_amount}",f"{str(deposit_details['balance'])}"]
        writer.writerow(field)
    return(render_template('success.html'))

@app.route('/withdrawal')
def withdrawal():
    return render_template('withdrawal_customer.html')

@app.route('/withdrawal_customer',methods=['POST'])
def withdrawal_customer():
    withdrawal_account_number = int(request.form['withdrawal_account_number'])
    withdrawal_amount = int(request.form['withdrawal_amount'])

    withdrawal_details = data_customer.find_one({'a_no':withdrawal_account_number})
    balance = int(withdrawal_details['balance'])
    data_customer.update_one({'a_no':withdrawal_account_number},{ "$set": { "balance": balance-withdrawal_amount }})
    withdrawal_details = data_customer.find_one({'a_no':withdrawal_account_number})
    # deposit_details['balance']= balance+deposit_amount
 
    withdrawali_details = account_data.find_one({'a_no':withdrawal_account_number})
    # print((depositor_details['name']))

    message = f"Hi {str(withdrawali_details['name'])},\nYour account has been debited Rs {withdrawal_amount}\nYour current balance is {str(withdrawal_details['balance'])}"
    with smtplib.SMTP_SSL("smtp.gmail.com",465) as server:
        server.login('prasoonyash@gmail.com','')
        server.sendmail('prasoonyash@gmail.com',str(withdrawali_details['email']),message)
    with open(f"{withdrawali_details['name']}.csv", 'a', newline='') as file:
        writer = csv.writer(file)
                
        field = [f"Withdarwal by {withdrawal_account_number}",f"{withdrawal_amount}",f"{str(withdrawal_details['balance'])}"]
        writer.writerow(field)
    return(render_template('success.html'))

@app.route('/balance_enquiry')
def balance_enquiry():
    cursor = data_customer.find_one({'a_no':session_account_number})
    balance = cursor['balance']
    return render_template('balance_show.html',balance=balance)

@app.route('/mini_statement')
def mini_statement():
    print(session_account_number)
    cursor = account_data.find_one({'a_no':session_account_number})
    print(cursor)
    name = cursor['name']
    # Connection.send_message(subject=f'Hi {name}\nMini Statement for account number {session_account_number}', recipients=f"{cursor[email]}", body="The Mini Statement is sent to your email", sender="prasoonyash@gmail.com", attachments=f"{cursor['name'].csv}")
    msg=Message("Hey your {name} mini statement is attached with this mail", recipients =cursor['email'] ,sender="prasoonyash@gmail.com" )
    msg.subject= f'Mini Statement for account number {session_account_number}'
    msg.attach = f"{cursor['name'].csv}"
    mail.send(msg)
    # with smtplib.SMTP_SSL("smtp.gmail.com",465) as server:
    #     server.login('prasoonyash@gmail.com','')
    #     server.sendmail('prasoonyash@gmail.com',str(cursor['email']),message)
    return render_template("success.html")
    

@app.route('/kyc')
def kyc():
    cursor = account_data.find_one({'a_no':session_account_number})
    return render_template('kyc.html',cursor=cursor)

    
    



if __name__ == "__main__":
    app.run(debug=True)