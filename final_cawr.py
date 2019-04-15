import pandas as pd
import numpy as np
from random import randint

user_count = 2
reco_count = 100
img_count = 2000
small_cell_count = 10
small_cell_capacity = 50
img_sizes = np.random.randint(low=4, high=13, size=(img_count,))

df_image_tags = pd.read_csv('image_tags_new.csv')
df_image_tags = df_image_tags[:img_count]
df_user_tags = pd.read_csv('user_tags_new.csv')

df_image_tags_norm = df_image_tags.div(df_image_tags.sum(axis=1), axis=0)
df_user_tags_norm = df_user_tags.div(df_user_tags.sum(axis=1), axis=0)

reco_matrix = np.zeros((user_count, reco_count))

def calc_initial_reco():
	global df_image_tags, df_user_tags, df_image_tags_norm, df_user_tags_norm
	df_image_tags = df_image_tags.T

	df_user_image = df_user_tags.dot(df_image_tags)
	df_matrix = df_user_image.as_matrix(columns=None)

	for i in range(user_count):
		reco_matrix[i]=sorted(range(len(df_matrix[i])),key=lambda x:df_matrix[i][x])[-reco_count:]
		reco_matrix[i] = reco_matrix[i][::-1]

	df_user_tags_norm=df_user_tags_norm.T
	df_image_tags_norm=df_image_tags_norm.T

	print("Initial reco matrix completed")

def calc_utility():
	w, h = img_count, user_count
	a = [[0 for x in range(w)] for y in range(h)] 
	for u in range(user_count):
		for i in range(img_count):
			sum_col=df_image_tags_norm[i]*df_user_tags_norm[u]
			sum_t=np.sum(sum_col)
			np_sq=np.sqrt(np.sum(df_image_tags_norm[i]))*np.sqrt(np.sum(df_user_tags_norm[u]))
			a[u][i]=sum_t/np_sq

	p_pref = pd.DataFrame(a)
	p_pref = p_pref.div(p_pref.sum(axis=1), axis=0)

	wr = np.random.uniform(low=0.5, high=0.7, size=(user_count,))

	p_pref_cpy = p_pref.copy()

	print("p_pref calculated")

	for j in range(user_count):
		for i in range(img_count):
			if i in reco_matrix[j]:
				p_pref_cpy.iloc[j][i] *= 2
			else:
				p_pref_cpy.iloc[j][i] /= 2

	p_pref_cpy = p_pref_cpy.div(p_pref_cpy.sum(axis=1), axis=0)
	p_rec = p_pref_cpy

	wr_df = pd.DataFrame(wr)

	p_req = p_rec.T.copy()
	p_not_req = p_pref.T.copy()

	print("p_rec calculated")

	for i in range(user_count):
		p_req.loc[:,i] *= wr_df.iloc[i][0]
		p_not_req.loc[:,i] *= (1-wr_df.iloc[i][0])   

	utility=p_req.T.sum(axis=0)
	utility=pd.DataFrame(utility)
	utility=utility.T

	print('utility calculated')

	return utility

def knapSack(wt, val, W, n): 
		K = [[0 for x in range(W + 1)] for x in range(n + 1)] 

		for i in range(n + 1): 
			for w in range(W + 1): 
				print("in ks: ", i, w, end='\r')

				if i == 0 or w == 0: 
					K[i][w] = 0

				elif wt.iloc[0][i-1] <= w: 
					K[i][w] = max(val.iloc[0][int(i-1)] + K[int(i-1)][int(w-wt.iloc[0][int(i-1)])],  K[int(i-1)][w]) 

				else: 
					K[i][w] = K[i-1][w]

		res = K[n][W] 
		P = []
		w = W 

		for i in range(n,0,-1): 
			if res <= 0: 
				break
			if w<0:
				break
			if res == K[int(i - 1)][int(w)]:
				continue
			else:
				P.append(int(i-1))
				res = res - val.iloc[0][int(i - 1)] 
				w = w - wt.iloc[0][int(i - 1)]

		return K[n][W], P

def cawr():
	image_size=pd.DataFrame(img_sizes)
	image_size=image_size.T

	calc_initial_reco()
	utility = calc_utility()
	knw, P = knapSack(image_size, utility, small_cell_capacity, reco_count)

	RC_in = reco_matrix

	cache =  np.random.choice(img_count, small_cell_count, replace=False)

	RC_f = [[], []]

	for u in range(user_count):
		RC_f[u]=list(set(RC_in[u]) & set(P))

	for u in range(user_count):
		if len(RC_f[u]) < 10: 
			for i in list(set(list(set(cache) & set(RC_in[u]))) - set(RC_f[u])):
				RC_f[u].append(i)
				
	for u in range(user_count):
		if len(RC_f[u]) < 10: 
			for i in list(set(RC_in[u]) - set(RC_f[u])):
				RC_f[u].append(i)

	return RC_f

print(cawr())