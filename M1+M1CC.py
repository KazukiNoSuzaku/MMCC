#Author: Kaustav Ghosh
#Student ID:720054122
#M1+M2/M/C/C Simulation (C=16)

import math
import numpy
import random 
import matplotlib.pyplot as plt
from matplotlib import figure
import pandas as pd

class Sim2():
  def __init__(self, Customer_total,mean_interarrival_Time1,mean_interarrival_Time2,mean_service_Time):
    self.mean_interarrival_FirstClass =mean_interarrival_Time1 # Mean Interarrival Time (1/λ1) NEW CELL
    self.mean_interarrival_SecondClass =mean_interarrival_Time2 # Mean Interarrival (1/λ2) HANDOVER
    self.threshold=2

    self.mean_service=mean_service_Time # Mean Service Time (1/µ) (Note : It should be considered that Mean Service Time < Mean Interarrival Time)
    self.sim_time = 0.0
    self.C_servers=16
    self.num_event = self.C_servers+2
    self.num_customers = 0
    self.num_customers_FirstClass=0
    self.num_customers_SecondClass=0
    self.num_customers_required = Customer_total
    
    self.server_status=numpy.zeros(self.C_servers+1)                                          
    self.area_server_status=numpy.zeros(self.C_servers)
    self.time_next_event = numpy.zeros(self.C_servers+2)
    self.time_next_event[0]=self.sim_time+self.expon(self.mean_interarrival_FirstClass)         #determine next arrival
    self.time_next_event[self.C_servers+1]=self.sim_time+self.expon(self.mean_interarrival_SecondClass)
    if self.time_next_event[0]<self.time_next_event[self.C_servers+1]:
      self.next_event_type=0
    else:
      self.next_event_type=self.C_servers+1
    for i in range(1,self.C_servers+1):
      self.time_next_event[i]=math.inf;
    self.server_idle=0        #determine next departure.
    self.server_utilization=numpy.zeros(self.C_servers)
    self.total_server_utilization=0
    self.Total_Loss=0
    self.Total_Loss_FirstClass=0
    self.Total_Loss_SecondClass=0

  ##########################  Define MAIN() function
  def main(self):
    while ((self.num_customers_FirstClass+self.num_customers_SecondClass) < self.num_customers_required):
      self.timing()
      self.update_time_avg_stats()
      if (self.next_event_type == 0):
        self.arrive_FirstClass()                      ## next event is First Class arrival
      elif (self.next_event_type == (self.C_servers+1)):
        self.arrive_SecondClass()                      ## next event is Second Class arrival
      else:  
        self.j=self.next_event_type
        self.depart()                       ## next event is departure
    self.report();
  #####################  Define TIMING() function
  def timing(self):
    self.min_time_next_event = math.inf
      ##Determine the event type of the next event to occur
    for i in range(0,self.num_event):
      if (self.time_next_event[i] <= self.min_time_next_event):
          self.min_time_next_event=self.time_next_event[i]
          self.next_event_type=i

    self.time_last_event=self.sim_time
     ##advance the simulation clock
    self.sim_time=self.time_next_event[self.next_event_type]

  ##################  Define UPDATE_TIME_AVG_STATS() function
  def update_time_avg_stats(self):
    self.time_past=self.sim_time-self.time_last_event
    for i in range(1,self.C_servers+1):
      self.area_server_status[i-1]+=self.time_past*self.server_status[i]

#########################   Define ARRIVE() function (First Class)
  def arrive_FirstClass(self):
    ix=0
    self.server_idle = 0
  ##Schedule next arrival
    self.time_next_event[0]=self.sim_time+self.expon(self.mean_interarrival_FirstClass)
    while (self.server_idle == 0 and ix<=self.C_servers):
      if (self.server_status[ix] == 0):
        self.server_idle = ix
      ix+=1
    if (self.server_idle != 0): ## Someone is IDLE
      self.server_status [self.server_idle] = 1
      self.time_next_event[self.server_idle] =self.sim_time+ self.expon(self.mean_service)
    else:               ## server is BUSY
      self.Total_Loss_FirstClass +=1
    self.num_customers_FirstClass+=1

  ############   Define ARRIVE() function (Second Class)

  def arrive_SecondClass(self):
    ix=0
    self.server_idle = 0
  ##Schedule next arrival
    self.time_next_event[self.C_servers+1]=self.sim_time+self.expon(self.mean_interarrival_SecondClass)
    while (self.server_idle == 0 and ix<=(self.C_servers-self.threshold)):
      if (self.server_status[ix] == 0):
        self.server_idle = ix
      ix+=1
    if (self.server_idle != 0): ## Someone is IDLE
      self.server_status [self.server_idle] = 1
      self.time_next_event[self.server_idle] =self.sim_time+ self.expon(self.mean_service)
    else:               ## server is BUSY
      self.Total_Loss_SecondClass +=1
    self.num_customers_SecondClass+=1

    ##################   Define DEPARTURE() function
  def depart(self):
      self.server_status [self.j] = 0
      self.time_next_event [self.j] = math.inf
     #########################   Define REPORT() function
  def expon(self,mean):
    return (-1*mean*math.log(random.random()))
 
  def report(self):
    for i in range(0,self.C_servers):
      self.server_utilization[i]=self.area_server_status[i]/self.sim_time
      self.total_server_utilization+=self.area_server_status[i]
    self.total_server_utilization = self.total_server_utilization/(self.sim_time*self.C_servers)
    print('')
    print('')
    print ('----------------------------------Simulation Report from this Simulation----------------------------------')
    print('')
    meu=1/self.mean_service
    lambda1=1/self.mean_interarrival_FirstClass
    lambda2=1/self.mean_interarrival_SecondClass
    self.CBP=self.Total_Loss_FirstClass/self.num_customers_FirstClass
    print('λ1 = ',lambda1)
    print('λ2 = ',lambda2)  
    print('µ = ',meu)
    print('')
    print('Total Server Utilization = ',self.total_server_utilization)
    print('Call Block Probablity = ',self.CBP)
    Temp1=0
    Temp2=0
    Temp3=0
    for i in range(0,self.C_servers-self.threshold+1):
      Temp1+=((1/math.factorial(i)) * (((lambda1+lambda2)/meu)**i))
    for i in range(self.C_servers-self.threshold+1,self.C_servers+1):
      Temp2+=((1/(math.factorial(i))) * (((lambda1+lambda2)/meu)**(self.C_servers-self.threshold)) * ((lambda1/meu)**(i-self.C_servers+self.threshold)))
    P0=1/(Temp1+Temp2)
    P02=1/(Temp1+Temp3)

    self.HFP = self.Total_Loss_SecondClass/self.num_customers_SecondClass
    #HFP=(1/(math.factorial(self.C_servers-self.threshold))) * (((lambda1+lambda2)/meu)**(self.C_servers-self.threshold)) *(1/math.factorial(self.threshold)) * ((lambda1/meu)**(self.threshold)) *P0
    print('Handover Failure Probability =',self.HFP)



obj = Sim2(Customer_total=100000,mean_interarrival_Time1=10,mean_interarrival_Time2=10,mean_service_Time=100)
obj.main()


l1=[]#store utilization
l2=[]#store CBP
l3=[]#Block HFP


#arrival rate .01 = 100 sec mean interarrival time 
print('')
print ('----------------------------------ABP < 0.02----------------------------------')
print('New call arrival rate = 0.1')
for i in range(10,101):
  obj = Sim2(Customer_total=100000,mean_interarrival_Time1=10,mean_interarrival_Time2=i,mean_service_Time=100)
  obj.main()
  x=obj.total_server_utilization
  y=obj.CBP
  z=obj.HFP
  l1.append(x)
  l2.append(y)
  l3.append(z)
  print(y,z,i)



###################### Storing data in CSV
df= pd.DataFrame()
df['Utilization']=l1
df['CBP']=l2
df['HFP']=l3

df.to_csv('Report_2.csv', index=False)





l1=[]#store utilization
l2=[]#store CBP
l3=[]#Block HFP
l4=[]#new cell rate


#arrival rate .01 = 100 sec mean interarrival time 
print('')
print ('----------------------------------ABP < 0.02----------------------------------')
print('handover rate =.03')
for i in range(10,101):
  obj = Sim2(Customer_total=100000,mean_interarrival_Time1=i,mean_interarrival_Time2=33,mean_service_Time=100)
  obj.main()
  x=obj.total_server_utilization
  y=obj.CBP
  z=obj.HFP
  l1.append(x)
  l2.append(y)
  l3.append(z)
  l4.append(1/i)
  print(y,z,i)



###################### Storing data in CSV
df= pd.DataFrame()
df['Utilization']=l1
df['CBP']=l2
df['HFP']=l3
df['ABP']=df['CBP']+ df['HFP']*10
df['NEW CELL']=l4

df.to_csv('Report_3.csv', index=False)