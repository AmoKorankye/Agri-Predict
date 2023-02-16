from __future__ import print_function
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report
from sklearn import metrics
from sklearn import tree
import warnings
import pickle
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

warnings.filterwarnings('ignore')


# page configuration
st.set_page_config(page_title = "Agri-Predict webapp", page_icon = ":tada:", layout = "wide")


# add css component
with open('styles.css') as f:
    st.markdown(f'<style>(f.read())</style>', unsafe_allow_html = True)
    
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("styles.css")


# Beta Version
with st.container():
    st.markdown("<p style = 'position: absolute; top: 0; right: 0; margin: 0; font-weight: bold; color: #000000; background-color: #FFFFFF; border: 1px solid #6eab3b; padding: 5px; padding-left: 10px; padding-right: 10px; border-radius: 20px;'> Beta Version </p>", unsafe_allow_html = True)
    st.image("header.png")


# Farmer Friendly Embedded System
with st.container():
    st.markdown("<h1 style = 'text-align: center; color: #7fcc2b'>Farmer Friendly Embedded System</h1>", unsafe_allow_html=True)
    st.markdown("<p style = 'text-align: center; font-weight: bold; font-size:20px;'>Agri-Predict is an embedded system and Machine Learning based model with the main focus of future crop forecasting</p>", unsafe_allow_html=True)
    st.write("##")


# farmer images 
with st.container():
    column_1, column_2, column_3 = st.columns(3)
    with column_1:
        st.image("women farming.jpg")
    with column_2:
        st.image("black farmer image.jpg")
    with column_3:
        st.image("farm.jpg")    

# Scroll to find out more
with st.container():
    st.write("##")
    st.markdown("<p style = 'position: absolute; top: 50%; right: 40%; left: 40%; margin: 0; font-weight: bold; color: #FFFFFF; background-color: #2ACC32; border: 1px solid #2ACC32; padding: 5px; padding-left: 40px; padding-right: 10px; border-radius: 10px;'> Scroll to find out more </p>", unsafe_allow_html = True)
    st.write("##")


left_column, right_column = st.columns(2)

# Agri Predict icon
with left_column:
    st.image("icon.png")


# About Section
with right_column:
    st.write("##")
    st.markdown("<p style = 'text-align: left; font-weight: bold; font-size:30px; color: #7fcc2b'>ABOUT</p>", unsafe_allow_html=True)
    st.markdown("<p style = 'text-align: left; font-weight: bold; '>Agri-Predict predicts the subsequent crop that will grow the best under the current soil and environmental circumstances, supplying the ideal nutrients and growth conditions at any given time. All the while enabling the farmer to remotely manage and watch over their farm. The goal of our project is to develop an accessible and self-sufficient model for modernizing farming methods and enhancing the output of agricultural products in Africa, both in terms of quantity and quality.</p>", unsafe_allow_html=True)


# Arduino Sensor Values
nitrogen_input = 10
phosphorus_input = 20
potassium_input = 30
temperature_input = 40
humidity_input = 50
pH_input = 60
rainfall_input = 70

# Machine Learning

PATH = 'Crop_recommendation.csv'
df = pd.read_csv(PATH)

features = df[['N', 'P','K','temperature', 'humidity', 'ph', 'rainfall']]
target = df['label']
labels = df['label']

df = pd.DataFrame(features)
input_data = df.values

acc = []
model = []


Xtrain, Xtest, Ytrain, Ytest = train_test_split(features,target,test_size = 0.2,random_state =2)

DecisionTree = DecisionTreeClassifier(criterion="entropy",random_state=2,max_depth=5)

DecisionTree.fit(Xtrain,Ytrain)

predicted_values = DecisionTree.predict(Xtest)
x = metrics.accuracy_score(Ytest, predicted_values)
acc.append(x)
model.append('Decision Tree')

DT_pkl_filename = 'DecisionTree.pkl'

DT_Model_pkl = open(DT_pkl_filename, 'wb')
pickle.dump(DecisionTree, DT_Model_pkl)

DT_Model_pkl.close()


NaiveBayes = GaussianNB()

NaiveBayes.fit(Xtrain,Ytrain)

predicted_values = NaiveBayes.predict(Xtest)
x = metrics.accuracy_score(Ytest, predicted_values)
acc.append(x)
model.append('Naive Bayes')
score = cross_val_score(NaiveBayes,features,target,cv=5)
NB_pkl_filename = 'NBClassifier.pkl'
NB_Model_pkl = open(NB_pkl_filename, 'wb')
pickle.dump(NaiveBayes, NB_Model_pkl)
NB_Model_pkl.close()

SVM = SVC(gamma='auto')

SVM.fit(Xtrain,Ytrain)

predicted_values = SVM.predict(Xtest)

x = metrics.accuracy_score(Ytest, predicted_values)
acc.append(x)
model.append('SVM')

score = cross_val_score(SVM,features,target,cv=5)

LogReg = LogisticRegression(random_state=2)

LogReg.fit(Xtrain,Ytrain)

predicted_values = LogReg.predict(Xtest)

x = metrics.accuracy_score(Ytest, predicted_values)
acc.append(x)
model.append('Logistic Regression')
score = cross_val_score(LogReg,features,target,cv=5)

LR_pkl_filename = 'LogisticRegression.pkl'
LR_Model_pkl = open(DT_pkl_filename, 'wb')
pickle.dump(LogReg, LR_Model_pkl)
LR_Model_pkl.close()


RF = RandomForestClassifier(n_estimators=20, random_state=0)
RF.fit(Xtrain,Ytrain)

predicted_values = RF.predict(Xtest)

x = metrics.accuracy_score(Ytest, predicted_values)
acc.append(x)
model.append('RF')
score = cross_val_score(RF,features,target,cv=5)

RF_pkl_filename = 'RandomForest.pkl'
RF_Model_pkl = open(RF_pkl_filename, 'wb')
pickle.dump(RF, RF_Model_pkl)
RF_Model_pkl.close()

data = np.array([[60,61,78,20.71219,19.83643,6.317153,94.0366]])
prediction = RF.predict(data)[0]
predictionPrint = prediction.upper()

# Sensor values
with st.container():
    st.write("##")
    st.write("---")
    st.write("##")
    st.markdown("<h1 style = 'text-align: left; color: #218225'>Sensor Values</h1>", unsafe_allow_html=True)
    column_1, column_2, column_3, column_4 = st.columns(4)
    
    with column_1:
        st.write("##")
        st.markdown("<p style = 'position: absolute; top: 0; left: 0; margin: 0; font-weight: bold; color: #000000; background-color: #FFFFFF; border: 1px solid #6eab3b; padding: 5px; padding-left: 10px; padding-right: 10px; border-radius: 20px;'> Nitrogen </p>", unsafe_allow_html = True)
        st.markdown(f"<p style = 'font-weight: bold; font-size: 30px; padding-top: 15px;'>{nitrogen_input} units</p>", unsafe_allow_html= True)
        st.write("##")
        st.write("##")
        st.markdown("<p style = 'position: absolute; top: 0; left: 0; margin: 0; font-weight: bold; color: #000000; background-color: #FFFFFF; border: 1px solid #6eab3b; padding: 5px; padding-left: 10px; padding-right: 10px; border-radius: 20px;'> Humidity </p>", unsafe_allow_html = True)
        st.markdown(f"<p style = 'margin-left: 0px; font-weight: bold; font-size: 30px; padding-top: 15px;'>{humidity_input} %</p>", unsafe_allow_html= True)
        st.write("##")
        st.write("##")
        
    with column_2:
        st.write("##")
        st.markdown("<p style = 'margin-left: 50px; position: absolute; top: 0; left: 0; margin: 0; font-weight: bold; color: #000000; background-color: #FFFFFF; border: 1px solid #6eab3b; padding: 5px; padding-left: 10px; padding-right: 10px; border-radius: 20px;'> Potassium </p>", unsafe_allow_html = True)
        st.markdown(f"<p style = 'margin-left: 6px; font-weight: bold; font-size: 30px; padding-top: 15px;'>{potassium_input} units</p>", unsafe_allow_html= True)
        st.write("##")
        st.write("##")
        st.markdown("<p style = 'margin-left: 0px; position: absolute; top: 0; left: 0; margin: 0; font-weight: bold; color: #000000; background-color: #FFFFFF; border: 1px solid #6eab3b; padding: 5px; padding-left: 10px; padding-right: 10px; border-radius: 20px;'> Temperature </p>", unsafe_allow_html = True)
        st.markdown(f"<p style = 'margin-left: 0px; font-weight: bold; font-size: 30px; padding-top: 15px;'>{temperature_input} °C</p>", unsafe_allow_html= True)
        st.write("##")
        st.write("##")
        
    with column_3:
        st.write("##")
        st.markdown("<p style = 'margin-left: 0px; position: absolute; top: 0; left: 0; margin: 0; font-weight: bold; color: #000000; background-color: #FFFFFF; border: 1px solid #6eab3b; padding: 5px; padding-left: 10px; padding-right: 10px; border-radius: 20px;'> Phosphorus </p>", unsafe_allow_html = True)
        st.markdown(f"<p style = 'margin-left: 0px; font-weight: bold; font-size: 30px; padding-top: 15px;'>{phosphorus_input} units</p>", unsafe_allow_html= True)
        st.write("##")
        st.write("##")
        st.markdown("<p style = 'margin-left: 0px; position: absolute; top: 0; left: 0; margin: 0; font-weight: bold; color: #000000; background-color: #FFFFFF; border: 1px solid #6eab3b; padding: 5px; padding-left: 10px; padding-right: 10px; border-radius: 20px;'> pH </p>", unsafe_allow_html = True)
        st.markdown(f"<p style = 'margin-left: 0px; font-weight: bold; font-size: 30px; padding-top: 15px;'>{pH_input} units</p>", unsafe_allow_html= True)
        st.write("##")
        st.write("##")


    with column_4:
        st.write("##")
        st.markdown("<p style = 'margin-left: 0px; position: absolute; top: 0; left: 0; margin: 0; font-weight: bold; color: #000000; background-color: #FFFFFF; border: 1px solid #6eab3b; padding: 5px; padding-left: 10px; padding-right: 10px; border-radius: 20px;'> Rainfall </p>", unsafe_allow_html = True)
        st.markdown(f"<p style = 'margin-left: 0px; font-weight: bold; font-size: 30px; padding-top: 15px;'>{rainfall_input} units</p>", unsafe_allow_html= True)
        st.write("##")
        st.write("##")
        st.write("##")
    
    # Prediction
    st.markdown("<h3 style = 'text-align: center; font-weight: bold; font-size: 30; color: #218225'> considering the current sensor values the best crop to grow is: </h3>", unsafe_allow_html=True)
    st.markdown(f"<h2 style = 'text-align: center; position: absolute; top: 50%; right: 40%; left: 40%; margin: 0; font-weight: bold; color: #FFFFFF; background-color: #2ACC32; border: 1px solid #2ACC32; padding: 5px; padding-left: 70px; padding-right: 10px; border-radius: 10px;'> {predictionPrint} </h2>", unsafe_allow_html = True)


# Contact form
st.write("##")
st.write("##")
st.write("##")
st.write("---")
st.markdown("<h1 style ='color: #218225; text-align: center;'>Contact Us</h1>", unsafe_allow_html= True)

with st.container():
    st.write("##")
    # Documention: https://formsubmit.co/ !!! CHANGE EMAIL ADDRESS !!!
    contact_form = """
    <form action="https://formsubmit.co/kwaku.amo-korankye@acity.edu.gh" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here" required></textarea>
        <button type="submit">Send</button>
    </form>
    """
    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown(contact_form, unsafe_allow_html=True)
    with right_column:
        st.empty()
        

# Tech Mind
col1, col2, col3 = st.columns(3)

with col2:
    st.write("##")
    st.write("##")
    st.write("##")
    st.image("Tech Mind.png")
