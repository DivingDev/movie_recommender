from flask import Flask, request, render_template
import pickle
import requests
movies = pickle.load(open('models/movies.pkl','rb'))
similarity = pickle.load(open('models/similarity.pkl', 'rb'))
new_df = pickle.load(open("models/movies_dict.pkl", 'rb'))


def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{id}?api_key=3fd2be6f0c70a2a598f084ddfb75487c&language=en-US".format(id = movie_id))
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/' + data["poster_path"]


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse = True, key=lambda x:x[1])[1:6]

    recommended_movies_poster = []
    recommend_movies = []

    for i in movies_list:
        # print(movies.iloc[i[0]].title)
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        # poster fetch
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommend_movies, recommended_movies_poster
    


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/recommendation", methods = ['GET', 'POST'])
def recommendation():
    if request.method == "POST":
        try:
            if request.form:
                movies_name = request.form['movies']
                print(movies_name)
                recommendation_list, poster_path = recommend(movies_name)
                for i in poster_path:
                    print(i)
                return render_template("prediction.html", recommendations = zip(recommendation_list,poster_path))
        except Exception as e:
            error = {'error':e}
            return render_template("prediction.html")
    else:
        return render_template("prediction.html")


if __name__ == '__main__':
    app.debug = True
    app.run()