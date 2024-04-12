import csv
import numpy as np

a = np.loadtxt(open('a.csv', "r"), delimiter=';')
M = np.loadtxt(open('M.csv', "r"), delimiter=';')
N = np.loadtxt(open('N.csv', "r"), delimiter=';')
MN_original = np.loadtxt(open('MN.csv', "r"), delimiter=';')


MN = np.dot(M, N)
aM = np.dot(a, M)
Ma = np.dot(M, a)

print(MN)
print(aM)
print(Ma)