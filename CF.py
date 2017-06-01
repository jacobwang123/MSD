import graphlab as gl

def evaluate(test, recomm):
    recall_sum = 0
    precision_sum = 0
    user_list = list(test['user_id'].unique())

    for user in user_list:
        r_score = 0
        p_score = 0
        test_subset = test[test['user_id']==user]
        recomm_subset = recomm[recomm['user_id']==user]
        for test_item in test_subset['song_id']:
            for recomm_item in recomm_subset:
                if test_item == recomm_item:
                    r_score += 1
        for recomm_item in test_subset['song_id']:
            for test_item in recomm_subset:
                if test_item == recomm_item:
                    p_score += 1
        user_recall = r_score / len(test_subset[0])
        user_precision = p_score / 5
        recall_sum += user_recall # What ratio of items that a user likes were actually recommended.
        precision_sum += user_precision # Out of all the recommended items, how many the user actually liked?

    return recall_sum / len(user_list), precision_sum / len(user_list)

def main():
    ratings_train = gl.SFrame.read_csv('train_triplets.txt', delimiter='\t', header=False)
    ratings_test = gl.SFrame.read_csv('visible_evaluation_triplets.txt', delimiter='\t', header=False)
    ratings_train.rename({'X1': 'user_id', 'X2':'song_id', 'X3':'rating'})
    ratings_test.rename({'X1': 'user_id', 'X2':'song_id', 'X3':'rating'})
    
    # CF model
    item_sim_model = gl.item_similarity_recommender.create(ratings_train, user_id='user_id', item_id='song_id', target='rating', similarity_type='cosine')
    
    item_sim_recomm = item_sim_model.recommend(users=ratings_test['user_id'], k=5)
    
    print(evaluate(ratings_test, item_sim_recomm))

if __name__ == '__main__':
    main()