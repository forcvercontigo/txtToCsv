# -*- coding: utf-8 -*-
 
import os
import shutil 
#make new folder
#example : mk('data0','King-ASR-098')

def mk(name,path=os.getcwd()):
	os.makedirs(path+'/'+name)
	os.makedirs(path+'/'+name+'/train')
	os.makedirs(path+'/'+name+'/dev')
	os.makedirs(path+'/'+name+'/test')


#get folder in this dir
def getfolder(path=os.getcwd()):
	file=os.listdir(path)
	folder=[]
	for i in file:
		if os.path.isdir(i):
			folder.append(i)
	return folder
folder_name = getfolder()
print(folder_name)
#get txt file name
def gettxt(path):
	l=[]
	for root, dirs, files in os.walk(path):
		for file in files:
			if os.path.splitext(file)[1]=='.txt':
				l.append(os.path.join(root,file))
	return l
	print()


#get file name of all data,including root
#script [] is folder name of scipts
def file_name(file_dir=os.getcwd()):
	txts=[]
	wavs=[]
	script=[]
	for root, dirs, files in os.walk(file_dir):
		if root.endswith('SCRIPT'):
			script.append(root)
		for file in files:
			if os.path.splitext(file)[1]=='.txt':
				txts.append(os.path.join(root,file))
			if os.path.splitext(file)[1]=='.TXT':
				txts.append(os.path.join(root,file))
			if os.path.splitext(file)[1]=='.WAV':
				wavs.append(os.path.join(root,file))
			if os.path.splitext(file)[1]=='.wav':
				wavs.append(os.path.join(root,file))
	return txts,wavs,script

txts=[]
wavs=[]
script=[]
txts,wavs,script=file_name()
#in every script folder,need to find the corresponding wav folder,i is path of every script folder
number = 0
multi_file = 0
now_path = os.getcwd()
print(now_path)
for i in script:
	#print('i=',i)
	dir_wave=i[:-6]
	dir_wave=dir_wave+'WAVE'#wav folder name
	#print('dir_wav=',dir_wave)
	for root, dirs, files in os.walk(i):
		for file in files:
			#print('file=',file)
			name=file[:-4]#remove the string '.txt'
			#print('script name=',name)
			for root2, dirs2, files2 in os.walk(dir_wave):#search in wav folder
				#print(root2,'#######',name)
				if root2.endswith(name)|root2.endswith(name.upper()):
					for root3, dirs3, files3 in os.walk(root2):#find the corresponding wav folder
						print('root',root)
						#print('files',files)
						#print('root2',root2)
						#print('name',name)
						#print('root3',root3)
						#print('files3',files3)
						if not files3==[]:
							#copy the whole folder
							new_path = now_path+'/'+str(number)+'/'+name+'/'
							new_file = now_path+'/'+str(number)+'/'+name+'.txt'
							if os.path.isdir(new_path):
								shutil.copytree(root3,now_path+'/'+str(number)+'/'+name+str(multi_file)+'/')
								multi_file=multi_file+1
							else:
								shutil.copytree(root3,new_path)
							print('from')
							print(root+'/'+file)
							print('to')
							print(new_file)
							if os.path.isfile(new_file):
								shutil.copy(root+'/'+file,now_path+'/'+str(number)+'/'+str(multi_file)+name)
								multi_file=multi_file+1
							else:
								shutil.copy(root+'/'+file,new_file)
							number=number+1
							print(number)
		

				
			
		

	

	




		















