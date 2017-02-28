# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 03:55:32 2015


@author: nasseh
"""

# This program is called data_set_conditioner. It gets rid noise and excessive data point.

import csv
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import polynomial as P
import pickle
import os

 
file_list=[]
d=open('master_setup.txt','r')
for line in d:
    temp=line.split(',')
    temp[1:6]=map(float,temp[1:6]) # get rid of end character and turn numbers into float
    if temp[0][0]=='#' or temp[0][0]=='%': #this if statement ignors the lines in master_setup file that begin with '#' or '%'.
        pass
    else:
        file_list.append(temp)

current_dir=os.getcwd()
A=os.listdir(current_dir)
if 'working_directory' not in A:        
    os.makedirs(current_dir+'/working_directory')

output = open(current_dir+'/working_directory/file_list_conditioned.pkl', 'wb')    
pickle.dump(file_list, output)      
output.close()  

time_master=[]
temp_master=[]
dil_master=[]
k=0

for var in file_list:
#    if sys.platform[0:5]=='linux':
#        try:
#            Data=open('/media/nasseh/FE0E012C0E00E00F/Science_Backup/Results/Python_Dil_analysis/Fitting_real_function/'+var[0],'rb')
#        except:
#            Data=open('/home/nasseh/Desktop/Python_Dil_analysis/Fitting_real_function/'+var[0],'rb')
#    else:
#        Data =  open('G:\\Science_Backup\\Results\\Python_Dil_analysis\\Fitting_real_function\\'+var[0], 'rb')
    
    Data=open(var[0],'r')
    D= csv.reader(Data)
    t = []
    temp = []
    dil = []
    for row in D:
        t.append(row[0])
        temp.append(row[1])
        dil.append(row[2])
    del t[0],temp [0] ,dil [0]
    Data.close()

    t = np.array(map(float,t))
    temp = np.array(map(float,temp))
    dil =np.array(map(float,dil))*1E-6
    time_master.append(t)
    temp_master.append(temp)
    dil_master.append(dil)
    del t, temp, dil, row

reg_order=2 #The order of polynomial used in noise filtering. Higher sr better have higher reg-order
def regresser(bottom,center,top):
    time_reg=time_fit[center]
    coef1= P.polyfit(time_fit[bottom:top],temp_fit[bottom:top],reg_order)
    temp_reg=P.polyval(time_fit[center],coef1)
    coef1= P.polyfit(time_fit[bottom:top],dil_fit[bottom:top],reg_order)
    dil_reg=P.polyval(time_fit[center],coef1)
    regressed_point=[time_reg,temp_reg,dil_reg]
    return regressed_point
start=0
time_cond=[] #conditioned time data
temp_cond=[]
dil_cond=[]

time_cond_master=[] #master file that has all of the conditioned time data
temp_cond_master=[]
dil_cond_master=[]

regressed_point_list=[]

for i in xrange(len(time_master)):
    print i
    time_cond.append(time_master[i][0])
    temp_cond.append(temp_master[i][0])
    dil_cond.append(dil_master[i][0])
    time_fit=time_master[i]
    dil_fit=dil_master[i]
    temp_fit=temp_master[i]
    points=[]
    for j in xrange(1,len(time_master[i])):
        if abs(time_fit[j]-time_cond[-1])>=10:
            points.append(j)
            time_cond.append(time_fit[j])          
        elif abs(temp_fit[j]-temp_cond[-1])>=3:
            points.append(j)
            temp_cond.append(temp_fit[j])
    regressed_point_list.append(points)   
time_cond=[]
temp_cond=[]
dil_cond=[]         
for i in xrange(len(time_master)):
    time_cond=[]
    temp_cond=[]
    dil_cond=[]    
    time_cond.append(time_master[i][0])
    temp_cond.append(temp_master[i][0])
    dil_cond.append(dil_master[i][0])
    time_fit=time_master[i]
    dil_fit=dil_master[i]
    temp_fit=temp_master[i]
    points=regressed_point_list[i]
    for j in xrange(1,len(points)-1):
        regressed=regresser(points[j-1],points[j],points[j+1])
        time_cond.append(regressed[0])
        temp_cond.append(regressed[1])
        dil_cond.append(regressed[2])
    time_cond_master.append(time_cond) 
    temp_cond_master.append(temp_cond)
    dil_cond_master.append(dil_cond)


output = open(current_dir+'/working_directory/time_conditioned.pkl', 'wb')    
pickle.dump(time_cond_master, output)      
output.close()        

output = open(current_dir+'/working_directory/temp_conditioned.pkl', 'wb')    
pickle.dump(temp_cond_master, output)      
output.close()

output = open(current_dir+'/working_directory/dil_conditioned.pkl', 'wb')    
pickle.dump(dil_cond_master, output)      
output.close()  
    
    
plt.figure(11)
for i in xrange(len(file_list)):
    plt.plot(time_master[i],dil_master[i], label=file_list[i][0])
    
for i in xrange(len(file_list)):
    plt.plot(time_cond_master[i],dil_cond_master[i],"o", label=file_list[i][0])
plt.legend()

plt.figure(12)
for i in xrange(len(file_list)):
    plt.plot(temp_master[i],dil_master[i], label=file_list[i][0])
    
for i in xrange(len(file_list)):
    plt.plot(temp_cond_master[i],dil_cond_master[i],"o", label=file_list[i][0])
plt.legend()

plt.figure(13)
for i in xrange(len(file_list)):
    plt.plot(time_master[i],temp_master[i],label=file_list[i][0])
    
for i in xrange(len(file_list)):
    plt.plot(time_cond_master[i],temp_cond_master[i],"o", label=file_list[i][0])
plt.legend()

