
# coding: utf-8




from pydub import AudioSegment
from pydub.silence import split_on_silence
import sys
import os
import time





def main():
    
    name = 'bbc.wav'
    sound = AudioSegment.from_mp3("bbc.mp3")
    sound.export(name, format="wav")
    sound = AudioSegment.from_wav(name)
    
    
    silence_thresh=-30    
    min_silence_len=400    
    length_limit=500    
    abandon_chunk_len=500   
    joint_silence_len=100  
    split(sound,silence_thresh,min_silence_len,length_limit,abandon_chunk_len,joint_silence_len)


:


def split(chunk,silence_thresh,min_silence_len,length_limit,abandon_chunk_len,joint_silence_len):
    print('start\\n',' *'*30)
    name = 'bbc.wav'
    chunks = split_on_silence(        chunk,min_silence_len=min_silence_len,silence_thresh=silence_thresh)
    
    
    
    for i in list(range(len(chunks)))[::-1]:
        if len(chunks[i])<=abandon_chunk_len:
            chunks.pop(i)
    

    
    chunks = chunk_join_length_limit(chunks,joint_silence_len=joint_silence_len,length_limit=length_limit)
    

    
    if not os.path.exists('./chunks'):os.mkdir('./chunks')
    namef,namec = os.path.splitext(name)
    namec = namec[1:]

    
    total = len(chunks)
    for i in range(total):
        new = chunks[i]
        save_name = '%s_%04d.%s'%(namef,i,namec)
        new.export('./chunks/'+save_name, format=namec)
        print('%04d'%i,len(new))
    print('saved')


# In[80]:


def chunk_join_length_limit(chunks,joint_silence_len,length_limit):
    
    # 
    silence = AudioSegment.silent(duration=joint_silence_len)
    adjust_chunks=[]
    temp = AudioSegment.empty()
    for chunk in chunks:
        print(adjust_chunks)
        length = len(temp)+len(silence)+len(chunk) 
        
        if length<5000:
            temp+=silence+chunk
        else: 
            adjust_chunks.append(temp)
            temp=chunk
    else:
        adjust_chunks.append(temp)
        
    return adjust_chunks





main()

