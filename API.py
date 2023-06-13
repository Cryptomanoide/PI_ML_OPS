from fastapi import FastAPI
import uvicorn
import pandas as pd

# Cargar los dataset en un DataFrame
merged_data = pd.read_csv(r'C:\Users\josgr\Desktop\PI_ML_OPS\Data transformada\movies.csv')


# Crear una instancia de la aplicación FastAPI
app = FastAPI()

# Definir las funciones para los endpoints de la API

@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes: str):
    # Filtrar las películas por mes y contar la cantidad
    cantidad = len(merged_data[merged_data['release_date'].str[5:7] == mes])
    return f"{cantidad} cantidad de películas fueron estrenadas en el mes de {mes}"

@app.get('/cantidad_filmaciones_dia/{dia}')
def cantidad_filmaciones_dia(dia: str):
    # Filtrar las películas por día y contar la cantidad
    cantidad = len(merged_data[merged_data['release_date'].str[8:10] == dia])
    return f"{cantidad} cantidad de películas fueron estrenadas en el día {dia}"

@app.get('/score_titulo/{titulo}')
def score_titulo(titulo: str):
    # Filtrar la película por título
    pelicula = merged_data[merged_data['title'] == titulo]

    if len(pelicula) == 0:
        return f"No se encontró la película con el título {titulo}"

    # Obtener el título, año de estreno y score
    titulo = pelicula['title'].values[0]
    anio_estreno = pelicula['release_date'].str[:4].values[0]
    score = pelicula['popularity'].values[0]

    return f"La película {titulo} fue estrenada en el año {anio_estreno} con un score/popularidad de {score}"

@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo: str):
    # Filtrar la película por título
    pelicula = merged_data[merged_data['title'] == titulo]

    if len(pelicula) == 0:
        return f"No se encontró la película con el título {titulo}"

    # Obtener la cantidad de votos y el valor promedio de votaciones
    votos_count = pelicula['vote_count'].values[0]
    vote_average = pelicula['vote_average'].values[0]

    if votos_count < 2000:
        return f"La película {titulo} no cumple con la cantidad mínima de votaciones (2000) y no se devuelve ningún valor."

    return f"La película {titulo} fue estrenada en el año {pelicula['release_date'].values[0][:4]}. La misma cuenta con un total de {votos_count} valoraciones, con un promedio de {vote_average}."

@app.get("/actor/{nombre_actor}")
def get_actor(nombre_actor):
    # Filtrar el dataset "credits" por nombre de actor
    actor_films = merged_data[merged_data['cast'].apply(lambda x: any(actor['name'] == nombre_actor and actor['job'] != 'Director' for actor in x))]

    if len(actor_films) == 0:
        return f"No se encontraron registros para el actor {nombre_actor}"

    # Obtener la cantidad de películas y el promedio de retorno del actor
    num_films = len(actor_films)
    total_return = 0
    for index, row in actor_films.iterrows():
        movie_id = row['id']
        movie_return = merged_data.loc[merged_data['id'] == movie_id, 'return'].values[0]
        total_return += movie_return

    average_return = total_return / num_films

    return f"El actor {nombre_actor} ha participado en {num_films} filmaciones. Ha conseguido un retorno total de {total_return} con un promedio de {average_return} por filmación."

@app.get("/director/{nombre_director}")
def get_director(nombre_director):
    # Filtrar el dataset "credits" por nombre de director
    director_films = merged_data[merged_data['crew'].apply(lambda x: any(crew['name'] == nombre_director and crew['job'] == 'Director' for crew in x))]

    if len(director_films) == 0:
        return f"No se encontraron registros para el director {nombre_director}"

    # Obtener el retorno total del director
    director_return = 0
    film_details = []

    for index, row in director_films.iterrows():
        movie_id = row['id']
        movie_return = merged_data.loc[merged_data['id'] == movie_id, 'return'].values[0]
        director_return += movie_return

        movie_title = merged_data.loc[merged_data['id'] == movie_id, 'title'].values[0]
        release_date = merged_data.loc[merged_data['id'] == movie_id, 'release_date'].values[0]
        budget = merged_data.loc[merged_data['id'] == movie_id, 'budget'].values[0]
        revenue = merged_data.loc[merged_data['id'] == movie_id, 'revenue'].values[0]

        film_details.append({
            'title': movie_title,
            'release_date': release_date,
            'return': movie_return,
            'budget': budget,
            'revenue': revenue
        })

    return {
        'director': nombre_director,
        'success': director_return,
        'film_details': film_details
    }


