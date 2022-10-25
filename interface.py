from flask import Flask,request,jsonify,render_template
import numpy as np
import json
import pickle
import config
from flask_mysqldb import MySQL

app = Flask(__name__)

####### MYSQL CONFIGURATION STEP########

app.config["MYSQL_HOST"] = "localhost"
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'AjayAjay1504'
app.config['MYSQL_DB']   = 'diab'
mysql = MySQL(app)

@app.route('/')
def Home_API():
    return render_template("index.html")


@app.route("/predict_diab",methods=["GET","POST"])
def pred():

    with open(config.MODEL_PATH,'rb') as f:
        knn_model = pickle.load(f)

    with open(config.DATA_PATH,'r') as f:
        knn_data = json.load(f)

    data = request.form

    test_array = np.zeros(len(knn_data['columns']))
    test_array[0] = eval(data['Pregnancies'])
    a = test_array[0]
    test_array[1] = eval(data['Glucose'])
    b = test_array[1]
    test_array[2] = eval(data['BloodPressure'])
    c = test_array[2]
    test_array[3] = eval(data['SkinThickness'])
    d = test_array[3]
    test_array[4] = eval(data['Insulin'])
    e = test_array[4]
    test_array[5] = eval(data['BMI'])
    f = test_array[5]
    test_array[6] = eval(data['DiabetesPedigreeFunction'])
    g = test_array[6]
    test_array[7] = eval(data['Age'])
    h = test_array[7]

    output = knn_model.predict([test_array])

    
    cursor = mysql.connection.cursor()
    query  = 'CREATE TABLE IF NOT EXISTS DIABETES(Pregnancies VARCHAR(20),Glucose VARCHAR(20),BloodPressure VARCHAR(20),SkinThickness VARCHAR(20),Insulin VARCHAR(20),BMI VARCHAR(20),DiabetesPedigreeFunction VARCHAR(20),Age VARCHAR(20),Outcome VARCHAR(20))'
    cursor.execute(query)
    cursor.execute('INSERT INTO DIABETES(Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,DiabetesPedigreeFunction,Age,Outcome) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)',(a,b,c,d,e,f,g,h,output))

    mysql.connection.commit()
    cursor.close()

    return render_template("index1.html",output=output)




 
if __name__ == "__main__":
    app.run(port=config.PORT_NO)


