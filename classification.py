import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
from sklearn.model_selection import train_test_split
from numpy import mean
from numpy import append as npappend
from numpy import array as nparray
from subprocess import call

with open('othersongs.csv', mode='r') as infile:
    reader = csv.reader(infile)
    song_dict = {rows[1].lower():rows[3].replace("\n", "") for rows in 
        reader}
    christmas_song_dict  = {k : v for k, v in song_dict.items() if
        "christmas" in k or "santa" in k or
        "xmas" in k or "reindeer" in k or
        "jingle bells" in k or "x-mas" in k}
    
with open("christmassongs.csv", mode='r') as infile:
    reader = csv.reader(infile)
    christmas_song_dict2 = {rows[0].lower():rows[1].replace("\n",
        "") for rows in reader if rows != []}
    total_xmas_song_dict = {**christmas_song_dict, **christmas_song_dict2}
    
song_dict = {k:v for k,v in song_dict.items() if
    k.lower() not in total_xmas_song_dict.keys()}
    
xmas_scores = [0 for _ in total_xmas_song_dict.keys()]
other_scores = [1 for _ in song_dict.keys()][:700]

y = xmas_scores + other_scores

all_texts = (list(total_xmas_song_dict.values()) +
    list(song_dict.values())[:700])
    
vectorizer = CountVectorizer(binary=True, lowercase=True)

counts = vectorizer.fit_transform(all_texts).todense()
features = vectorizer.get_feature_names()
X = counts
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
    
clf = DecisionTreeClassifier(max_depth=10)

clf.fit(X_train, y_train)
print(len(xmas_scores)/(len(xmas_scores) + len(other_scores)),
    clf.score(X_test, y_test))
    
export_graphviz(clf, out_file='tree.dot', 
                feature_names = features,
                class_names = ["christmas", "no_christmas"],
                rounded = True, proportion = False, 
                precision = 2, filled = True)
  
call(['dot', '-Tpng', 'tree.dot', '-o', 'tree.png', '-Gdpi=600'])

