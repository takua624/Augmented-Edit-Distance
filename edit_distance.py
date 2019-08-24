import os
import numpy as np
import time
import pandas as pd
from openpyxl import load_workbook
import xlsxwriter
from scipy.spatial.distance import euclidean

'''
% Edit Distance is a standard Dynamic Programming problem. Given two strings s1 and s2, the edit distance between s1 and s2 is the minimum number of operations required to convert string s1 to s2. The following operations are typically used:
% Replacing one character of string by another character.
% Deleting a character from string
% Adding a character to string
% Example:
% s1='article'
% s2='ardipo'
% EditDistance(s1,s2)
% > 4
% you need to do 4 actions to convert s1 to s2
% replace(t,d) , replace(c,p) , replace(l,o) , delete(e)
% using the other output, you can see the matrix solution to this problem
%
%
% by : Reza Ahmadzadeh (seyedreza_ahmadzadeh@yahoo.com - reza.ahmadzadeh@iit.it)
% 14-11-2012
'''

def edit_distance(s1, s2):
	m = len(s1)
	n = len(s2)
	v = np.zeros((m+1,n+1))
	for ii in range(m):
		v[ii+1,0]=ii+1
	for jj in range(n):
		v[0,jj+1]=jj+1
	for ii in range(m):
		for jj in range(n):
			if(s1[ii]==s2[jj]):
				v[ii+1,jj+1]=v[ii,jj]
			else:
				v[ii+1,jj+1]=1+min(min(v[ii+1,jj],v[ii,jj+1]),v[ii,jj])
	the_v = v[m,n]
	return (the_v,v)
