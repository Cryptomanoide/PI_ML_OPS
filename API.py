from fastapi import FastAPI
import uvicorn
import pandas as pd

# Cargar el DataFrame desde el archivo CSV
df = pd.read_csv('C:/Users/josgr/Desktop/PI_ML_OPS/api_data.csv')

# Crear la instancia de FastAPI
app = FastAPI()


@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes: str):
    # Filtra las películas por mes y cuenta la cantidad
    cantidad = len(df[df['release_date'].str[5:7] == mes])
    return f"{cantidad} cantidad de películas fueron estrenadas en el mes de {mes}"




# Endpoint para obtener la cantidad de filmaciones en un día específico
@app.get('/cantidad_filmaciones_dia/{dia}')
def cantidad_filmaciones_dia(dia: str):
    dia = dia.lower()
    cantidad = len(df[df['release_date'].str.endswith(f"-{dia}")])
    return f"{cantidad} cantidad de películas fueron estrenadas en los días {dia.capitalize()}"

# Endpoint para obtener el score de una película por su título
@app.get('/score_titulo/{titulo}')
def score_titulo(titulo: str):
    row = df[df['title'] == titulo]
    if not row.empty:
        return f"La película {row['title'].iloc[0]} fue estrenada en el año {row['release_year'].iloc[0]} con un score/popularidad de {row['popularity'].iloc[0]}"
    else:
        return f"No se encontró la película '{titulo}'"

# Endpoint para obtener la cantidad de votos y promedio de votaciones de una película
@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo: str):
    row = df[df['title'] == titulo]
    if not row.empty:
        votos = float(row['vote_count'].iloc[0])
        promedio = float(row['vote_average'].iloc[0])
        if votos >= 2000:
            return f"La película {row['title'].iloc[0]} fue estrenada en el año {row['release_year'].iloc[0]}. La misma cuenta con un total de {votos} valoraciones, con un promedio de {promedio}"
        else:
            return f"La película {row['title'].iloc[0]} fue estrenada en el año {row['release_year'].iloc[0]}. La misma no cumple con la condición de tener al menos 2000 valoraciones."
    else:
        return f"No se encontró la película '{titulo}'"
    
@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor: str):
    # Rellenar los valores NaN en la columna 'actors' con una cadena vacía
    df['actors'] = df['actors'].fillna('')

    # Filtrar el DataFrame por el nombre del actor
    actor_df = df[df['actors'].str.contains(nombre_actor, case=False)]

    # Crear una lista de resultados
    results = []
    for _, row in actor_df.iterrows():
        result = {
            'title': row['title'],
            'release_date': row['release_date'],
            'revenue': row['revenue'],
            'budget': row['budget'],
        }
        results.append(result)

    return {'actor': nombre_actor, 'movies': results}

@app.get('/get_director/{nombre_director}')
def get_director(nombre_director: str):
    # Filtrar el dataset "credits" por nombre de director
    director_films = df['director']

    if len(director_films) == 0:
        return f"No se encontraron registros para el director {nombre_director}"

    director_success = 0
    films_info = []

    for index, row in director_films.iterrows():
        movie_id = row['id']
        movie_info = df.loc[df['id'] == movie_id, ['title', 'release_date', 'return', 'budget', 'revenue']]

        if len(movie_info) > 0:
            movie_title = movie_info['title'].values[0]
            release_date = movie_info['release_date'].values[0]
            movie_return = movie_info['return'].values[0]
            movie_budget = movie_info['budget'].values[0]
            movie_revenue = movie_info['revenue'].values[0]

            director_success += movie_return
            films_info.append((movie_title, release_date, movie_return, movie_budget, movie_revenue))

    if len(films_info) == 0:
        return f"No se encontraron registros de películas para el director {nombre_director}"

    return {
        "director_name": nombre_director,
        "director_success": director_success,
        "films_info": films_info
    }






    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

