from django.shortcuts import render
from django.http import HttpResponse
import numpy as np
import psycopg2

def outliers(request):
    conn = psycopg2.connect(
    host="localhost",
    database="company",
    user="postgres",
    password="NANU@vel123"
    )

    cursor = conn.cursor()

    cursor.execute("SELECT height FROM employee")
    L=[]
    a=[]
    M=[]
    rows = cursor.fetchall()
    for row in rows:
        L.append(row)
    for i in range(0,len(L)):
         a.append(L[i][0])

    q1=np.percentile(a,25)
    q2=np.percentile(a,50)
    q3=np.percentile(a,75)
    iqr=q3-q1
    low=q1-1.5*iqr
    Mx=q3+1.5*iqr
    cursor.execute("Delete FROM employee where height < %s or height >%s",(low,Mx,))
    conn.commit()
    cursor.execute("SELECT * FROM employee")
    rows = cursor.fetchall()
    return  HttpResponse("outliers Removed succesfully",rows)
      
    cursor.close()
    conn.close()
