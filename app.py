import streamlit as st
import pickle
import pandas as pd
import requests
from streamlit_lottie import st_lottie

def load_lottie(url):
    r=requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}%7D?api_key=a155ead2e39d9044a9a1f9955cd14259&language=en-US".format(movie_id))
    dta = response.json()
    return "https://image.tmdb.org/t/p/w500/"+dta['poster_path']

def recommend(movie):
    mov_ind = movies[movies['title'] == movie].index[0]
    distances = similarity[mov_ind]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:8]

    recommended_movies=[]
    recommended_movies_poster=[]
    for i in movie_list:
        movie_id=movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)

        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster

mov_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(mov_dict)

similarity=pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')
lottie_cd=load_lottie("https://assets8.lottiefiles.com/packages/lf20_CTaizi.json")
left_column,rightcolumn=st.columns(2)
with left_column:
    st.subheader("Hi!! I am Abeera")

    st.write("This a movie recommender system. You give your movie choice and we will recommend you top 3 movies of similar genres that you might be interesed to binge watch!!")
    st.write("So are you ready?")
with rightcolumn:
    st_lottie(lottie_cd,height=300,key="movie")
smn = st.selectbox(
    'Which movie would you like to choose?',
    (movies['title'].values))

if st.button('Recommend'):
    recommendations,posters=recommend(smn)
    col1,col2,col3 = st.columns(3)

    with col1:
        st.text(recommendations[0])
        st.image(posters[0])
    with col2:
        st.text(recommendations[1])
        st.image(posters[1])
    with col3:
        st.text(recommendations[2])
        st.image(posters[2])


