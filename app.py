from flask import Flask, render_template, flash, request, session, send_file, redirect, url_for
from werkzeug.utils import secure_filename
import datetime
import mysql.connector
import sys
import pickle
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
app.config['DEBUG'] = True

@app.route("/")
def homepage():
    return render_template('index.html')

@app.route("/AdminLogin")
def AdminLogin():
    return render_template('AdminLogin.html')

@app.route("/UserLogin")
def UserLogin():
    return render_template('UserLogin.html')

@app.route("/NewUser")
def NewUser():
    return render_template('NewUser.html')

@app.route("/NewQuery1")
def NewQuery1():
    return render_template('NewQueryReg.html')

@app.route("/UploadDataset")
def UploadDataset():
    return render_template('ViewExcel.html')

@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1croprecomdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb ")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)

@app.route("/UserHome")
def UserHome():
    user = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1croprecomdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where username='" + user + "'")
    data = cur.fetchall()
    return render_template('UserHome.html', data=data)

@app.route("/UQueryandAns")
def UQueryandAns():
    uname = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1croprecomdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Querytb where UserName='" + uname + "' and DResult='waiting'")
    data = cur.fetchall()
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1croprecomdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Querytb where UserName='" + uname + "' and DResult !='waiting'")
    data1 = cur.fetchall()
    return render_template('UserQueryAnswerinfo.html', wait=data, answ=data1)

@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    error = None
    if request.method == 'POST':
        if request.form['uname'] == 'admin' or request.form['password'] == 'admin':
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1croprecomdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb ")
            data = cur.fetchall()
            return render_template('AdminHome.html', data=data)
        else:
            return render_template('index.html', error=error)

@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1croprecomdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:
            alert = 'Username or Password is wrong'
            render_template('goback.html', data=alert)
        else:
            print(data[0])
            session['uid'] = data[0]
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1croprecomdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where username='" + username + "' and Password='" + password + "'")
            data = cur.fetchall()
            return render_template('UserHome.html', data=data)

@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        name1 = request.form['name']
        gender1 = request.form['gender']
        Age = request.form['age']
        email = request.form['email']
        pnumber = request.form['phone']
        address = request.form['address']
        uname = request.form['uname']
        password = request.form['psw']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1croprecomdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO regtb VALUES ('" + name1 + "','" + gender1 + "','" + Age + "','" + email
            + "','" + pnumber + "','" + address + "','" + uname + "','" + password + "')")
        conn.commit()
        conn.close()
        return render_template('UserLogin.html')

@app.route("/newquery", methods=['GET', 'POST'])
def newquery():
    if request.method == 'POST':
        uname = session['uname']
        nitrogen = request.form['nitrogen']
        phosphorus = request.form['phosphorus']
        potassium = request.form['potassium']
        temperature = request.form['temperature']
        humidity = request.form['humidity']
        ph = request.form['ph']
        rainfall = request.form['rainfall']
        location = request.form['select']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1croprecomdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Querytb VALUES ('','" + uname + "','" + nitrogen + "','" + phosphorus +
            "','" + potassium + "','" + temperature + "','" + humidity + "','" + ph
            + "','" + rainfall + "','waiting',',','" + location + "')")
        conn.commit()
        conn.close()
        uname = session['uname']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1croprecomdb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM Querytb where UserName='" + uname + "' and DResult='waiting'")
        data = cur.fetchall()
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1croprecomdb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM Querytb where UserName='" + uname + "' and DResult !='waiting'")
        data1 = cur.fetchall()
        return render_template('UserQueryAnswerinfo.html', wait=data, answ=data1)

@app.route("/excelpost", methods=['GET', 'POST'])
def uploadassign():
    if request.method == 'POST':
        file = request.files['fileupload']
        file_extension = file.filename.split('.')[1]
        print(file_extension)
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns

        df = ''
        if file_extension == 'xlsx':
            df = pd.read_excel(file.read(), engine='openpyxl')
        elif file_extension == 'xls':
            df = pd.read_excel(file.read())
        elif file_extension == 'csv':
            df = pd.read_csv(file)
        print(df)

        sns.countplot(df['label'], label="Count")
        plt.savefig('static/images/out.jpg')
        iimg = 'static/images/out.jpg'
        print(df)

        sns.countplot(df['label'], label="Count")
        plt.show()

        df.label = df.label.map({'rice': 0, 'maize': 1, 'chickpea': 2, 'kidneybeans': 3,
                                  'pigeonpeas': 4, 'mothbeans': 5, 'mungbean': 6, 'blackgram': 7,
                                  'lentil': 8, 'pomegranate': 9, 'banana': 10, 'mango': 11,
                                  'grapes': 12, 'watermelon': 13, 'muskmelon': 14, 'apple': 15,
                                  'orange': 16, 'papaya': 17, 'coconut': 18, 'cotton': 19,
                                  'jute': 20, 'coffee': 21})

        df_copy = df.copy(deep=True)
        df_copy[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']] = df_copy[
            ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']].replace(0, np.NaN)

        from sklearn.model_selection import train_test_split
        df.drop(df.columns[np.isnan(df).any()], axis=1)
        X = df.drop(columns='label')
        y = df['label']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)

        from sklearn.neural_network import MLPClassifier
        from sklearn.metrics import classification_report
        classifier = MLPClassifier(random_state=0)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)
        print(classification_report(y_test, y_pred))
        clreport = classification_report(y_test, y_pred)
        print("Accuracy on training set: {:.2f}".format(classifier.score(X_train, y_train)))
        print("Accuracy on test set: {:.3f}".format(classifier.score(X_test, y_test)))
        Tacc = "Accuracy on training set: {:.2f}".format(classifier.score(X_train, y_train))
        Testacc = "Accuracy on test set: {:.3f}".format(classifier.score(X_test, y_test))

        filename = 'crop-prediction-rfc-model.pkl'
        pickle.dump(classifier, open(filename, 'wb'))
        print("Training process is complete Model File Saved!")
        df = df.head(200)
        return render_template('ViewExcel.html', data=df.to_html(), dataimg=iimg,
                               Tacc=Tacc, testacc=Testacc, report=clreport)

@app.route("/AdminQinfo")
def AdminQinfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1croprecomdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Querytb where DResult='waiting'")
    data = cur.fetchall()
    return render_template('AdminQueryInfo.html', data=data)

@app.route("/answer")
def answer():
    Answer = ''
    Prescription = ''
    id = request.args.get('lid')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1croprecomdb')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Querytb where id='" + id + "'")
    data = cursor.fetchone()
    if data:
        UserName = data[1]
        nitrogen = data[2]
        phosphorus = data[3]
        potassium = data[4]
        temperature = data[5]
        humidity = data[6]
        ph = data[7]
        rainfall = data[8]
    else:
        return 'Incorrect username / password !'

    nit = float(nitrogen)
    pho = float(phosphorus)
    po = float(potassium)
    te = float(temperature)
    hu = float(humidity)
    phh = float(ph)
    ra = float(rainfall)

    filename = 'crop-prediction-rfc-model.pkl'
    classifier = pickle.load(open(filename, 'rb'))
    data = np.array([[nit, pho, po, te, hu, phh, ra]])
    my_prediction = classifier.predict(data)
    print(my_prediction)
    crop = ''
    fertilizer = ''

    if my_prediction == 0:
        Answer = 'Predict'
        crop = 'rice'
        fertilizer = '4 kg of gypsum and 1 kg of DAP/cent can be applied at 10 days after sowing'
    elif my_prediction == 1:
        Answer = 'Predict'
        crop = 'maize'
        fertilizer = 'The standard fertilizer recommendation for maize consists of 150 kg ha-1 NPK 14-23-14 and 50 kg ha-1 urea'
    elif my_prediction == 2:
        Answer = 'Predict'
        crop = 'chickpea'
        fertilizer = 'The generally recommended doses for chickpea include 20-30 kg nitrogen (N) and 40-60 kg phosphorus (P) ha-1. If soils are low in potassium (K), an application of 17 to 25 kg K ha-1 is recommended'
    elif my_prediction == 3:
        Answer = 'Predict'
        crop = 'kidneybeans'
        fertilizer = 'It needs good amount of Nitrogen about 100 to 125 kg/ha'
    elif my_prediction == 4:
        Answer = 'Predict'
        crop = 'pigeonpeas'
        fertilizer = 'Apply phosphorus fertilizer at sowing time. Recommended dose is 60 kg P2O5/ha'
    elif my_prediction == 17:
        Answer = 'Predict'
        crop = 'papaya'
        fertilizer = 'Generally 90 g of Urea, 250 g of Super phosphate and 140 g of Muriate of Potash per plant are recommended for each application'
    elif my_prediction == 18:
        Answer = 'Predict'
        crop = 'coconut'
        fertilizer = 'Organic Manure @50kg/palm or 30 kg green manure, 500 g N, 320 g P2O5 and 1200 g K2O/palm/year in two split doses during September and May'
    elif my_prediction == 19:
        Answer = 'Predict'
        crop = 'cotton'
        fertilizer = 'N-P-K 20-10-10 per hectare during sowing (through the sowing machine)'
    elif my_prediction == 20:
        Answer = 'Predict'
        crop = 'jute'
        fertilizer = 'Apply 10 kg of N at 20 - 25 days after first weeding and then again on 35 - 40 days after second weeding as top dressing'
    elif my_prediction == 21:
        Answer = 'Predict'
        crop = 'coffee'
        fertilizer = 'Coffee trees need a lot of potash, nitrogen, and a little phosphoric acid. Spread the fertilizer in a ring around each Coffee plant'
    else:
        Answer = 'Predict'
        crop = 'Crop info not Found!'

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1croprecomdb')
    cursor = conn.cursor()
    cursor.execute("UPDATE Querytb SET DResult='" + crop + "' WHERE id='" + id + "'")
    conn.commit()
    conn.close()

    return render_template('AnswerPage.html', answer=Answer, crop=crop, fertilizer=fertilizer)


if __name__ == '__main__':
    app.run(debug=True)
