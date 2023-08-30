import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px


# Load data from csv
df = pd.read_csv(r'https://github.com/NutchaponMet/DashBoard_streamlit/blob/main/datatset/RetailDataTransactions.csv')

def rfm_analysis(DataFrame):
    currentDate = datetime.now()
    df['trans_date'] = pd.to_datetime(df['trans_date'])
    def recency(x):
        return (currentDate - x.max()).days
    rfm = DataFrame.groupby('customer_id')\
            .agg({'trans_date':recency,'customer_id':'count','tran_amount':sum})\
            .rename(columns={'trans_date':'recency','customer_id':'frequency','tran_amount':'monetary'})
    return rfm


def display_data(DataFrame):
    show =  DataFrame.head(5)
    return show

def distribution_plot(DataFrame):
    rfm_data = rfm_analysis(df)
    pass



if __name__=='__main__':
    st.header('Hello World')
    st.subheader('This is my first dashboard with Streamlit!!!!')

    st.bar_chart(df['customer_id'].value_counts())
    select_visual = st.selectbox('What are visualizerion.',('Defualt','RFM Analysis'))
    col1, col2 = st.columns(2)
    if select_visual == 'Defualt':
        s = print(df.info())
        col1.dataframe(display_data(df),  height=250, width=600)
        col2.write(
            '''
            ข้อมูลเริ่มต้นจะถูกจัดเก็บให้อยู่ในรูปของราย transaction
            โดย ข้อมูลที่สนใจจะประกอบไปด้วย 
            \n**รหัสลูกค้า**
            \n**วันที่เข้ามารับบริการ**
            \n**และการใช้จ่ายในแต่ละครั้ง**
            '''
        )
    if select_visual == 'RFM Analysis':
        s = rfm_analysis(df).info()
        col1.dataframe(rfm_analysis(df).head(5),height=250, width=600)
        col2.write(
            '''
            ตารางนี้จะเป็นการนำข้อมูลดิบมาทำการแปลงให้อยู่ในรูปแบบ
            ที่สามารถวิเคราะห์ได้ โดย 
            \n*recency* หมายถึง จำนวนวันที่เข้ามาใช้บริการล่าสุด
            หาได้จากการนำวันที่ลูกค้ามาใช้บริการครั้งล่าสุด มาลบกับวันที่ปัจจุบัน
            \n*frequency* หมายถึง จำนวนครั้งที่เข้ามาใช้บริการหรือซื้อของ
            \n*monetary* หมายถึง จำนวนเงินที่ลูกค้าคนนั้นเข้ามาใช้บริการกับเรา 
            '''
        )
        select_analysis = st.selectbox('Analysis',('Distribution', 'Kmean clustering'))
        if select_analysis == 'Distribution':
            rfm_data = rfm_analysis(df)
            fig = px.scatter(x=rfm_data['frequency'],y=rfm_data['monetary'])
            st.subheader('Scatter Plot')
            st.plotly_chart(fig)
        if select_analysis =='Kmean clustering':
            pass
