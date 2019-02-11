# -*- coding: utf-8 -*-
#2019-01-29
#
#This file will automatically convert txt to csv file .
#Input: transcript file as txt format.Output:two csv file ,true sentence and one is actual sentence()
#Source wave input =$SOURCE/kingxx//DATA/(CHANNEL0,1,2)/wav/SPEARKxxx/(SESSION)/xxx.wav
#Source script input = /kingxx/*/script/SPEARKxx.txt
#Target script input = $TARGET/kingxx/(CHANNEL0,1,2)/wav/SPEARKxxx
#Target script output=$TARGET/kingxx/(CHANNEL0,1,2)/wav/SPEARKxxx.csv
#TARGET ACTUAL VOICE SCRIPT OUTPUT = $TARGET/kingxx-actual/(CHANNEL0,1,2)/wav/SPEARKxxx-Actual.csv
#
#Step1:
#move this file into a folder including：source data,
#such as :***/dataset/txt2csv.py(this file),King-ASR-098,King-ASR-102,.......
#Step2:
#cd  ~/dataset
#python txt2csv.py

import os
import shutil
import codecs
import csv
path=os.getcwd()
HOME=path
dirs=[]
def getDirList( p ):
	p = str( p )
	if p=="":
		return []
	if p[-1] != "/":
		p = p+"/"
	a = os.listdir( p )
	b = [ x   for x in a if os.path.isdir( p + x ) ]
	return b

#get txt file name
def get_txt(path=dirs):
	l=[]
	for root, dirs, files in os.walk(path):
		for file in files:
			if os.path.splitext(file)[1]=='.txt':
				l.append(os.path.join(root,file))
			if os.path.splitext(file)[1]=='.TXT':
				l.append(os.path.join(root,file))
	return l

def sentence(txt_dir):
	with codecs.open(txt_dir, 'rb') as f:
		sentence_set=[]
		sentence=[]
		for line in f.readlines():
			line=line.decode('utf-8-sig')
			sentence=line.split('\t')
			sentence_set.append(sentence)
	return sentence_set

def sent2list(sentence_set):
	num=[]
	csv=[]
	csv1=[]
	csv2=[]
	flag = 0
	for sentence in sentence_set:
		flag=flag+1
		#print(len(sentence))
		if flag%2 == 1:
			num.append(sentence[0])
		if len(sentence) > 0:
			csv.append(sentence[1])
	flag = 0
	for line in csv:
		if flag%2 == 0:
			csv1.append(csv[flag])
		else:
			csv2.append(csv[flag])
		flag = flag + 1
	return num,csv1,csv2




def write2csv(num,csv_file,csv_name='temp.csv'):
	with open(csv_name,"w") as csvfile: 
		writer = csv.writer(csvfile) 

		file_name = os.path.split(csv_name)[0].replace('SCRIPT','WAVE')+'/'
		floder_name = os.path.split(csv_name)[1].split('.')[0]
		print(file_name+'/'+floder_name+'/')
		

		writer.writerow(["wav_filename","transcript"]) #columns_name 


		for i in range(len(num)):
			writer.writerow([file_name+str(num[i]).strip()+'.wav',csv_file[i].lower().strip()])#save into csv file
		return csv_name
def get_wave_dir(root):
	l=root.split('/')
	indx=l.index('WAVE')
	wave_dir=''
	for i in range(indx+1):
		wave_dir=wave_dir+l[i]
		wave_dir=wave_dir+'/'
	#print(wave_dir)
	return wave_dir
def move_transcript(csv_name):
	path,name=os.path.split(csv_name)
	path=path[0:-7]
	path_set=[]
	for root, dirs, files in os.walk(path):
		for file in files:
			if file.endswith('wav'):
				path_set.append(get_wave_dir(root))
				get_wave_dir(root)
			if file.endswith('.WAV'):
				path_set.append(get_wave_dir(root))
	path_set2=list(set(path_set))
	if not os.path.exists(path_set2[0]):
		shutil.move(csv_name, path_set2[0])
	os.remove(csv_name)


def move2other_folder(csv_name,path):
	path=path+'/'
	if not os.path.exists(path):
		if os.makedirs(path):
			p=os.makedirs(path)
	if not os.path.exists(path):
		shutil.move(csv_name,path)
	os.remove(csv_name)

#get all txt file path

txts=get_txt(HOME)

#print(txts)
#for every txt file in list txts
for i in txts:
	#remove repeated showing of txts 
	sentence_set=sentence(i)
	#cdivide into 2 csv file,one is transcript and the other is actual sentence
	num,csv1,csv2=sent2list(sentence_set)
	#convert the first to csv 
	csv_name=write2csv(num,csv1,i[:-4]+'.csv')
	#move to wave folder
	move_transcript(csv_name)
	#convert the second to csv 
	csv_name=write2csv(num,csv2,i[:-4]+'actual.csv')
	#create a new path
	path=os.path.split(i)[0].replace('King','King-Actual')
	#move to new path folder
	move2other_folder(csv_name,path)
print('finished')




