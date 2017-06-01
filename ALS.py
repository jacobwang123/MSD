import pandas as pd
import numpy as np

def get_error(Q, X, Y, W):
	return np.sum((W * (Q - np.dot(X, Y)))**2)

def make_recommendations(W, Q, Q_hat):
	Q_hat -= np.min(Q_hat)
	Q_hat *= float(5) / np.max(Q_hat)
	song_ids = np.argmax(Q_hat - 5 * W, axis=1)
	with open('/Users/jacob/Desktop/Python/MSD/results.txt', 'w') as outfile:
		for jj, song_id in zip(range(m), song_ids):
			r = '{} : {} - {}\n'.format(jj + 1, song_id, Q_hat[jj, song_id])
			outfile.write(r)


if __name__ == '__main__':
	col = ['user_id','song_id','rating']
	# train_triplets
	df = pd.read_csv('/Users/jacob/Desktop/Python/MSD/train_triplets.txt', header=None, sep='\t', names=col)
	df['user_id'] = df['user_id'].astype('category')
	cat_columns = df.select_dtypes(['category']).columns
	df[cat_columns] = df[cat_columns].apply(lambda x: x.cat.codes)
	df['song_id'] = df['song_id'].astype('category')
	cat_columns = df.select_dtypes(['category']).columns
	df[cat_columns] = df[cat_columns].apply(lambda x: x.cat.codes)

	rp = df.pivot_table(columns=['song_id'], index=['user_id'], values='rating')
	rp = rp.fillna(0)

	Q = rp.values
	W = Q>0.5
	W[W == True] = 1
	W[W == False] = 0
	# To be consistent with Q matrix
	W = W.astype(np.float64, copy=False)

	lambda_ = 0.1
	n_factors = 100
	m, n = Q.shape
	n_iterations = 20

	X = 5 * np.random.rand(m, n_factors) 
	Y = 5 * np.random.rand(n_factors, n)

	errors = []
	for ii in range(n_iterations):
		X = np.linalg.solve(np.dot(Y, Y.T) + lambda_ * np.eye(n_factors), np.dot(Y, Q.T)).T
		Y = np.linalg.solve(np.dot(X.T, X) + lambda_ * np.eye(n_factors), np.dot(X.T, Q))
		errors.append(get_error(Q, X, Y, W))
	Q_hat = np.dot(X, Y)
	make_recommendations(W, Q, Q_hat)