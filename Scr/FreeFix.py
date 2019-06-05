# To store and manipulate the data 
import pandas as pd 

# To do linear algebra
import numpy as np 

# Plotting and visualization Library
import matplotlib.pyplot as plt
import seaborn as sns

# To check if a string contains the specified search pattern
import re

# Compute distance between each pair of the two collections of input
from scipy import spatial

# To import images to jupyter notebook
from IPython.display import Image

# To ignore warnings
import warnings
warnings.filterwarnings('ignore')

from wordcloud import WordCloud, STOPWORDS #used to generate world cloud

import json





df_ratings = pd.read_csv("../Input/ratings.csv")
df_links = pd.read_csv("../Input/links.csv")
df_tags = pd.read_csv("../Input/tags.csv")
df_movies = pd.read_csv("../Input/movies.csv")





# Creating a variable name user_ratings_total that will contain all the ratings that a specific userid 
# rated(.groupby) and we will also add(.agg) the ratings size and mean([np.size, np.mean]).
user_ratings_total = df_ratings.groupby(['userId']).agg({'rating': [np.size, np.mean]})
user_ratings_total.reset_index(inplace=True)  # To reset multilevel (pivot-like) index
#user_ratings_total.head(2)





# Creating a variable name movie_ratings_total  that will contain all the ratings that a specific movieid 
# has(.groupby) and we will also add(.agg) the ratings size and mean([np.size, np.mean]).
movie_ratings_total = df_ratings.groupby(['movieId']).agg({'rating': [np.size, np.mean]})
movie_ratings_total.reset_index(inplace=True)
#movie_ratings_total.head(2)






# Merging df_movies with movie_ratings_total
df_movies_final = df_movies.merge(movie_ratings_total, left_on='movieId', right_on='movieId', how='left')

# Changing names on columns
df_movies_final.columns = ['movieId', 'title', 'genres', 'rating_count', 'rating_avg']





def get_year(title):
    result = re.search(r'\(\d{4}\)', title)
    if result:
        found = result.group(0).strip('(').strip(')')
    else: 
        found = 0
    return int(found)
    
df_movies_final['year'] = df_movies_final.apply(lambda x: get_year(x['title']), axis=1)




# List of genres
genres_list = [
  "Action",
  "Adventure",
  "Animation",
  "Children",
  "Comedy",
  "Crime",
  "Documentary",
  "Drama",
  "Fantasy",
  "Film-Noir",
  "Horror",
  "Musical",
  "Mystery",
  "Romance",
  "Sci-Fi",
  "Thriller",
  "War",
  "Western",
  "(no genres listed)"
]




# Creating a function that will be filled by [0,1] based on the actual movie genres.
def set_genres_matrix(genres):
    movie_genres_matrix = []
    movie_genres_list = genres.split('|')
    for x in genres_list:
        if (x in movie_genres_list):
            movie_genres_matrix.append(1)
        else:
            movie_genres_matrix.append(0) 
    return movie_genres_matrix





    # Applying set_genres_matrix function to add a genres_matrix column to the df_movies_final
df_movies_final['genres_matrix'] = df_movies_final.apply(lambda x: np.array(list(set_genres_matrix(x['genres']))), axis=1)





def set_rating_group(number_of_ratings):
    if (number_of_ratings is None): return 0
    if (1 <= number_of_ratings <= 10): return 1
    elif (11 <= number_of_ratings <= 30): return 2
    elif (31 <= number_of_ratings <= 100): return 3
    elif (101 <= number_of_ratings <= 300): return 4
    elif (301 <= number_of_ratings <= 1000): return 5
    elif (1001 <= number_of_ratings): return 6
    else: return 0

df_movies_final['rating_group'] = df_movies_final.apply(lambda x: set_rating_group(x['rating_count']), axis=1)
df_movies_final.fillna(0, inplace=True)  # Replace NaN values to zero





# Stopwords are the English words which does not add much meaning to a sentence. 
# They can safely be ignored without sacrificing the meaning of the sentence.
#def get_stop_words():
stop_words = ['a', 'about', 'above', 'above', 'across', 'after', 'afterwards', 'again', 'against', 'all', 'almost', 
        'alone', 'along', 'already', 'also','although','always','am','among', 'amongst', 'amoungst', 'amount',  'an', 'and', 
        'another', 'any','anyhow','anyone','anything','anyway', 'anywhere', 'are', 'around', 'as',  'at', 'back','be','became', 
        'because','become','becomes', 'becoming', 'been', 'before', 'beforehand', 'behind', 'being', 'below', 'beside', 'besides', 
        'between', 'beyond', 'bill', 'both', 'bottom','but', 'by', 'call', 'can', 'cannot', 'cant', 'co', 'con', 'could', 'couldnt', 
        'cry', 'de', 'describe', 'detail', 'do', 'done', 'down', 'due', 'during', 'each', 'eg', 'eight', 'either', 'eleven','else', 
        'elsewhere', 'empty', 'enough', 'etc', 'even', 'ever', 'every', 'everyone', 'everything', 'everywhere', 'except', 'few', 'fifteen', 
        'fify', 'fill', 'find', 'fire', 'first', 'five', 'for', 'former', 'formerly', 'forty', 'found', 'four', 'from', 'front', 'full', 
        'further', 'get', 'give', 'go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', 'hereupon', 
        'hers', 'herself', 'him', 'himself', 'his', 'how', 'however', 'hundred', 'ie', 'if', 'in', 'inc', 'indeed', 'interest', 'into', 'is', 'it', 
        'its', 'itself', 'keep', 'last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made', 'many', 'may', 'me', 'meanwhile', 'might', 'mill', 
        'mine', 'more', 'moreover', 'most', 'mostly', 'move', 'much', 'must', 'my', 'myself', 'name', 'namely', 'neither', 'never', 'nevertheless',
        'next', 'nine', 'no', 'nobody', 'none', 'noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of', 'off', 'often', 'on', 'once', 'one', 
        'only', 'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out', 'over', 'own','part', 'per', 'perhaps', 'please', 
        'put', 'rather', 're', 'same', 'see', 'seem', 'seemed', 'seeming', 'seems', 'serious', 'several', 'she', 'should', 'show', 'side', 'since', 
        'sincere', 'six', 'sixty', 'so', 'some', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhere', 'still', 'such', 'system', 
        'take', 'ten', 'than', 'that', 'the', 'their', 'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 'therefore', 'therein', 
        'thereupon', 'these', 'they', 'thickv', 'thin', 'third', 'this', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus', 'to', 
        'together', 'too', 'top', 'toward', 'towards', 'twelve', 'twenty', 'two', 'un', 'under', 'until', 'up', 'upon', 'us', 'very', 'via', 'was', 
        'we', 'well', 'were', 'what', 'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon', 
        'wherever', 'whether', 'which', 'while', 'whither', 'who', 'whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with', 'within', 'without', 'would', 
        'yet', 'you', 'your', 'yours', 'yourself', 'yourselves', 'the']




tags_dict = {}

for index, x in df_tags.iterrows():
    word_list = str(x['tag']).lower().split(' ')
    movieId = x['movieId']
    for y in word_list:
        if y not in stop_words:
            if movieId in tags_dict:
                # if y not in tagsDict[movieId]:  # Switched off (we will get a non unique list)
                    tags_dict[movieId].append(y)
            else:
                tags_dict[movieId] = [y]

df_tags.apply(lambda x: str(x['tag']).split(' '), axis=1)
#print(tags_dict[1])




title_words_dict = {}

for index, x in df_movies.iterrows():
    word_list = str(x['title']).lower().split(' ')
    movieId = x['movieId']
    for y in word_list:
        if y not in stop_words:
            if movieId in title_words_dict:
                title_words_dict[movieId].append(y)
            else:
                title_words_dict[movieId] = [y]
#print(title_words_dict[1])





# Assigning 
# Parameter weights

genresSimilarityWeight = 0.8
tagsSimilarityWeight = 2
titleSimilarityWeight = 1
ratingAvgWeight = 0.2
ratingGroupWeight = 0.005
yearDistanceWeight = 0.1








def tags_similarity(basisMovieID, checkedMovieID, checkType):    
    # The higher value is the more similar (from 0 to 1) 
    if checkType == 'tag':
        dictToCheck = tags_dict
    else:
        dictToCheck = title_words_dict
        
    counter = 0
    if basisMovieID in dictToCheck: 
        basisTags = dictToCheck[basisMovieID]
        countAllTags = len(basisTags)
        basisTagsDict = {}
        for x in basisTags:
            if x in basisTagsDict:
                basisTagsDict[x] += 1
            else:
                basisTagsDict[x] = 1   
        
        for x in basisTagsDict:
            basisTagsDict[x] = basisTagsDict[x] / countAllTags
    else: return 0
    
    if checkedMovieID in dictToCheck: 
        checkedTags = dictToCheck[checkedMovieID]
        checkedTags = set(checkedTags) # Make the list unique
        checkedTags = list(checkedTags)
        
    else: return 0
    
    for x in basisTagsDict:
        if x in checkedTags: counter += basisTagsDict[x]
    return counter
    
def check_similarity(movieId):
    
    print("SIMILAR MOVIES TO:")
    print (df_movies_final[df_movies_final['movieId'] == movieId][['title', 'rating_count', 'rating_avg']])
    basisGenres = np.array(list(df_movies_final[df_movies_final['movieId'] == movieId]['genres_matrix']))
    basisYear = int(df_movies_final[df_movies_final['movieId'] == movieId]['year'])
    basisRatingAvg = df_movies_final[df_movies_final['movieId'] == movieId]['rating_avg']
    basisRatingGroup = df_movies_final[df_movies_final['movieId'] == movieId]['rating_group']
    
    moviesWithSim = df_movies_final
    moviesWithSim['similarity'] = moviesWithSim.apply(lambda x: 
                                                      spatial.distance.cosine(x['genres_matrix'], basisGenres) * genresSimilarityWeight + 
                                                      - tags_similarity(movieId, x['movieId'], 'tag') * tagsSimilarityWeight +
                                                      - tags_similarity(movieId, x['movieId'], 'title') * titleSimilarityWeight +
                                                      abs(basisRatingAvg - x['rating_avg']) * ratingAvgWeight +
                                                      abs(basisRatingGroup - x['rating_group']) * ratingGroupWeight + 
                                                      abs(basisYear - x['year'])/100 * yearDistanceWeight
                                                     , axis=1)
    
    moviesWithSim = moviesWithSim.loc[(moviesWithSim.movieId != movieId)]
    return moviesWithSim[['movieId', 'title', 'genres', 'rating_count', 'rating_avg', 'similarity']].sort_values('similarity')





movie_user_wants = input('Enter a movie: ')

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def movie(x):
    movies = list(df_movies_final['title'])
    for movie in movies:
        if fuzz.partial_ratio(x,movie) == 100:
            x = movie
    return x


result = df_movies_final.loc[df_movies_final['title'] == movie(movie_user_wants)]
movie__id__= int(result['movieId'])

similarityResult1  = check_similarity(movie__id__)
print(similarityResult1.head())


