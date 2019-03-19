import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

path = 'G:\工作\maildir\\allen-p\\all_documents\\'

def read(path):
    print(path)
    for dirpath,_,filenames in os.walk(path):
        email_list = []
        for i in filenames:
            message = ''
            email = {}
            with open(dirpath+i) as f:
                lines = f.readlines()
                for line in lines:
                    if ' Forwarded by' in line:
                        continue
                    if ':' not in line:
                        message += line.strip()
                        if len(message) == 0:
                            continue
                        email['body'] = message
                    else:
                        continue
                email_list.append(email)

    return email_list

def dict2csv(email_list):
    body_list = []
    for i in email_list:
        if 	len(i) != 1:
            continue
        body_list.append(i['body'])
    return body_list


def top_tfidf_feats(row, features, top_n=20):
    print(row)
    topn_ids = np.argsort(row)[::-1][:top_n]
    top_feats = [(features[i], row[i]) for i in topn_ids]
    df = pd.DataFrame(top_feats, columns=['features', 'score'])
    return df
#从所有的邮件中获取顶级术语（top terms）
def top_feats_in_doc(X, features, row_id, top_n=50):
    row = np.squeeze(X[row_id].toarray())
    return top_tfidf_feats(row, features, top_n)
def top_mean_feats(X, features,grp_ids=None, min_tfidf=0.1, top_n=25):
    if grp_ids:
        D = X[grp_ids].toarray()
    else:
        D = X.toarray()
    D[D < min_tfidf] = 0
    tfidf_means = np.mean(D, axis=0)
    return top_tfidf_feats(tfidf_means, features, top_n)
def top_feats_per_cluster(X, y, features, min_tfidf=0.1, top_n=25):
    dfs = []
    labels = np.unique(y)
    for label in labels:
        ids = np.where(y == label)
        feats_df = top_mean_feats(X, features, ids, min_tfidf=min_tfidf, top_n=top_n)
        feats_df.label = label
        dfs.append(feats_df)
    return dfs
email_list = read(path)
body_list = dict2csv(email_list)
name = ['content']
data = [body_list]
data = np.reshape(data,(-1,1))
data = pd.DataFrame(columns = name,data = data)
data.to_csv('G:\工作\maildir\data.csv',encoding = 'gbk')
#TF-IDF是术语词频–逆向文件频率（term frequency–inverse document frequency ）
vect = TfidfVectorizer()
X = vect.fit_transform(body_list)
#DTM(文献-检索词矩阵)进行二维表示。
X_dense = X.todense()
coords = PCA(n_components=2).fit_transform(X_dense)
#plt.scatter(coords[:, 0], coords[:, 1], c='m')
#plt.show()
features = vect.get_feature_names()
top_feats_in_doc(X, features, 1, 100)
top = top_mean_feats(X, features, top_n=100)
n_clusters = 3
clf = KMeans(n_clusters=n_clusters, max_iter=100, init='k-means++', n_init=1)
labels = clf.fit_predict(X)
red = [[],[]]
green = [[],[]]
blue = [[],[]]

for i in range(len(labels)):
    item = [coords[i][0],coords[i][1]]
    if labels[i] == 0:
        red[0].append(coords[i][0])
        red[1].append(coords[i][1])
        continue
    if labels[i] == 1:
        green[0].append(coords[i][0])
        green[1].append(coords[i][1])
        continue
    if labels[i] == 2:
        blue[0].append(coords[i][0])
        blue[1].append(coords[i][1])
        continue
plt.scatter(red[0],red[1],c='r')
plt.scatter(green[0],green[1],c='g')
plt.scatter(blue[0],blue[1],c='b')
#plt.show()
dfs = top_feats_per_cluster(X,labels,features,top_n=30)
plt.close('all')
x = dfs[0]['features']
y = dfs[0]['score']
plt.subplot(131)
plt.barh(x,y)
x = dfs[1]['features']
y = dfs[1]['score']
plt.subplot(132)
plt.barh(x,y)
x = dfs[2]['features']
y = dfs[2]['score']
plt.subplot(133)
plt.barh(x,y)
plt.show()
