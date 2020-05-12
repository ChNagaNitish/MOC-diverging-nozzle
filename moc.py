import numpy as np
import math
import sys
from os import system, remove
import time
gamma = float(input("Enter gamma >>> "))
M_entry = float(input("Enter Entry Mach Number >>> "))
M_exit = float(input("Enter Exit Mach Number >>> "))
height_throat = float(input("Enter the throat height of the nozzle >>> "))
N = int(input("Enter number of points >>> "))
#gamma = 1.4
#M_entry = 1.0000001
#M_exit = 2.487
height = height_throat/2#19.74/2
#N = 100
if M_entry==1.0:
	M_entry = 1.00001
start = time.time()
def nufromM(Mach):
	return np.sqrt((gamma+1)/(gamma-1))*math.atan(np.sqrt((Mach**2-1)*(gamma-1)/(gamma+1)))-math.atan(np.sqrt(Mach**2-1))
def Mfromnu(Nu):
	Nu_inf = np.pi*0.5*(np.sqrt(6)-1)
	var = (Nu/Nu_inf)**(2/3)
	A = 1.3604
	B = 0.0962
	C = -0.5127
	D = -0.6722
	E = -0.3278
	return (1+A*var+B*var**2+C*var**3)/(1+D*var+E*var**2)
nu_entry = nufromM(M_entry)
nu_exit = nufromM(M_exit)
mu_entry = math.asin(1/M_entry)
mu_exit = math.asin(1/M_exit)
theta_max = (nu_exit-nu_entry)/2
nu_inter = theta_max+nu_entry
M_inter = Mfromnu(nu_inter)
mu_inter = math.asin(1/M_inter)
theta_fan = (mu_entry+theta_max-mu_inter)
theta_N = N - 1
theta_delta = theta_max/theta_N
char_k = np.zeros(N)
for i in range(0,N):
	char_k[i] = nu_entry + 2*theta_delta*i 
nu_all = np.zeros((N,N))
theta_all = np.zeros((N,N))
M_all = np.zeros((N,N))
mu_all = np.zeros((N,N))
slope_L = np.zeros((N,N))
slope_R = np.zeros((N,N))
C_L = np.zeros((N,N))
C_R = np.zeros((N,N))
x_all = np.zeros((N,N))
y_all = np.zeros((N,N))
t_delta = theta_fan/theta_N
for i in range(0,N):
	slope_R[0][i] = np.tan(np.pi-(mu_entry-t_delta*i))
	C_R[0][i] = height
for i in range(0,N):
	for j in range(i,N):
		nu_all[i][j] = (char_k[j]+char_k[i])/2
		theta_all[i][j] = (char_k[j]-char_k[i])/2
		M_all[i][j] = Mfromnu(nu_all[i][j])
		mu_all[i][j] = math.asin(1/M_all[i][j])
for i in range(0,N):
	for j in range(i,N):
		slope_L[i][j] = np.tan(theta_all[i][j]+mu_all[i][j])
for i in range(1,N):
	for j in range(i,N):
		slope_R[i][j] = np.tan(theta_all[i][j]-mu_all[i][j])
for i in range(0,N-1):
	x_all[i][i] = -C_R[i][i]/slope_R[i][i]
	C_L[i][i] = y_all[i][i]-slope_L[i][i]*x_all[i][i]
	for j in range(i,N-1):
		x_all[i][j+1] = (C_R[i][j+1]-C_L[i][j])/(slope_L[i][j]-slope_R[i][j+1])
		y_all[i][j+1] = slope_R[i][j+1]*x_all[i][j+1]+C_R[i][j+1]
		C_L[i][j+1] = y_all[i][j+1]-slope_L[i][j+1]*x_all[i][j+1]
		C_R[i+1][j+1] = y_all[i][j+1]-slope_R[i+1][j+1]*x_all[i][j+1]
	if i==N-2:
		k = N-1
		x_all[k][k] = -C_R[k][k]/slope_R[k][k]
		C_L[k][k] = y_all[k][k]-slope_L[k][k]*x_all[k][k]
nozzle = np.zeros((N+1,2))
nozzle[0][0] = 0
nozzle[0][1] = height
slope_noz = np.zeros(N+1)
C_noz = np.zeros(N+1)
slope_noz[0] = np.tan(theta_max)
C_noz[0] = height
for i in range(1,N+1):
	slope_noz[i] = np.tan(theta_all[i-1][N-1])
for i in range(1,N+1):
	nozzle[i][0] = (C_noz[i-1]-C_L[i-1][N-1])/(slope_L[i-1][N-1] - slope_noz[i-1])
	nozzle[i][1] = slope_noz[i-1]*nozzle[i][0] + C_noz[i-1]
	C_noz[i] = nozzle[i][1]-slope_noz[i]*nozzle[i][0]
np.savetxt('nozzle_contour.dat',nozzle)
#np.savetxt('xpoints.dat',x_all)
#np.savetxt('ypoints.dat',y_all)
end = time.time()
print("\n\n\nTotal Time taken =",end-start,"seconds\n\n\n")