import argparse
import re
import os
import csv
import math
import collections as coll


def parse_argument():
    """
    Code for parsing arguments
    """
    parser = argparse.ArgumentParser(description='Parsing a file.')
    parser.add_argument('--train', nargs=1, required=True)
    parser.add_argument('--test', nargs=1, required=True)
    args = vars(parser.parse_args())
    return args


def parse_file(filename):
    """
    Given a filename outputs user_ratings and movie_ratings dictionaries

    Input: filename

    Output: user_ratings, movie_ratings
        where:
            user_ratings[user_id] = {movie_id: rating}
            movie_ratings[movie_id] = {user_id: rating}
    """
    user_ratings = {}
    movie_ratings = {}
    with open(filename) as fp:
        for line in fp:
	    movie, user, rating = line.strip().split(",")
            rating = float(rating)
            user = int(user)
            movie = int(movie)
	    if user not in user_ratings:
                user_ratings[user] = {}
            user_ratings[user][movie] = rating
            if movie not in movie_ratings:
                movie_ratings[movie] = {}
            movie_ratings[movie][user] = rating
    return user_ratings, movie_ratings


def compute_average_user_ratings(user_ratings):
    """ Given a the user_rating dict compute average user ratings

    Input: user_ratings (dictionary of user, movies, ratings)
    Output: ave_ratings (dictionary of user and ave_ratings)
    """
    ave_ratings = {}
    for user in user_ratings:
	num_ratings = 0
	rating_sum = 0.0
	for movie in user_ratings[user]:
	    num_ratings += 1
	    rating_sum += user_ratings[user][movie]		
        ave_ratings[user] = rating_sum / float(num_ratings)
    return ave_ratings


def compute_user_similarity(d1, d2, ave_rat1, ave_rat2):
    """ Computes similarity between two users

        Input: d1, d2, (dictionary of user ratings per user) 
            ave_rat1, ave_rat2 average rating per user (float)
        Ouput: user similarity (float)
    """
    num_commun_mov = 0
    sim_numerator = 0.0
    sim_denom_user1 = 0.0
    sim_denom_user2 = 0.0
    for movie in d1:
        if movie in d2:
            num_commun_mov += 1
            a1 = d1[movie] - ave_rat1
            a2 = d2[movie] - ave_rat2
            sim_numerator += a1*a2
            sim_denom_user1 += a1**2
            sim_denom_user2 += a2**2
    if num_commun_mov == 0:
        return 0.0
    denom = math.sqrt(sim_denom_user1 * sim_denom_user2)
    if denom == 0.0:
        return 0.0
    return sim_numerator / denom


def predict_ratings(movie_ratings_test, ave_ratings, movie_ratings, user_ratings):
    # pre-processting
    sim = {}
    counter = 0
    rmse = 0.0
    mae = 0.0
    f = open("predictions.txt", 'wt')
    writer = csv.writer(f)
    for movie in movie_ratings_test:
        if movie in movie_ratings:
            for user in movie_ratings_test[movie]:
                if user in ave_ratings:
                    label = movie_ratings_test[movie][user]
                    rating = ave_ratings[user]
                    nomin = 0.0
                    denomin = 0.0
                    for user1 in movie_ratings[movie]:
                        delta = movie_ratings[movie][user1] - ave_ratings[user1]
			key = (user, user1)
                        if user1 < user:
                            key = (user1, user)
                        if key not in sim:
                            d1 = user_ratings[user]
                            d2 = user_ratings[user1]
                            s = compute_user_similarity(d1, d2, ave_ratings[user], ave_ratings[user1])
                            sim[key] = s
			user_sim = sim.get(key, 0.0)
                        nomin += user_sim * delta
                        denomin += abs(user_sim)
                    rating += nomin / (denomin + 0.000001)
                    #print(movie, user, label, rating)
                    rmse += (label - rating)**2
                    mae += abs(label - rating)
                    counter += 1
                    writer.writerow((movie, user, label, rating))
    f.close()
    mae /= float(counter)
    print("RMSE %.4f" % math.sqrt(rmse / float(counter)))
    print("MAE %.4f" % mae)

def main():
    """
    This function is called from the command line via
    
    python cf.py --train [path to filename] --test [path to filename]
    """
    args = parse_argument()
    train_file = args['train'][0]
    test_file = args['test'][0]
    print train_file, test_file
    user_ratings, movie_ratings = parse_file(train_file)
    ave_ratings = compute_average_user_ratings(user_ratings)
    user_ratings_test, movie_ratings_test = parse_file(test_file)
    predict_ratings(movie_ratings_test, ave_ratings, movie_ratings, user_ratings)


if __name__ == '__main__':
    main()

