from fastapi import FastAPI
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

#Funcion de recomendacion de juegos

def similitud(id):
    df=pd.read_parquet("Datasets/data.parquet")
    df['app_name']=df['app_name'].str.strip()
    if df[df['id']==id].empty:
        return "El juego no se encuentra en la base de datos"
    df.reset_index(drop=True, inplace=True)

    #Vectorizar el nombre de los productos
    vectorizer=TfidfVectorizer()
    tfidf_matrix=vectorizer.fit_transform(df[['app_name','genres','tags']].apply(lambda x: ' '.join(x),axis=1))

    #Calcular la matriz de similitud del coseno
    similarity_matrix=cosine_similarity(tfidf_matrix)

    producto_index=df[df['id']==id].index[0]
    product_similarities=similarity_matrix[producto_index]
    most_similar_products_index=np.argsort(-product_similarities)[1:6]
    most_similar_products=df.loc[most_similar_products_index,'app_name']
    return most_similar_products

app = FastAPI()

@app.get("/developer_reviews_analysis/{desarrollador}",description="Devuelve un diccionario con el nombre del desarrollador y la cantidad de reviews positivas y negativas")
async def developer_reviews_analysis( desarrollador : str ):
    desarrollador=desarrollador.title()
    df=pd.read_parquet("Datasets/developers.parquet")
    respuesta=df[df['developer']==desarrollador][['Positive','Negative']].sum()
    respuesta = [f"{k} = {v}" for k, v in respuesta.items()]
    if desarrollador not in df["developer"].values:
        return {"respuesta" : "Desarrollador no encontrado"}
    else:
        return {"respuesta" : respuesta}

@app.get("/recomendacion_juego/{id_producto}",description="Devuelve una lista con 5 juegos similares al juego ingresado")
async def recomendacion_juego( id_producto : int ):

    respuesta=similitud(id_producto)
   
    return {"Recomendacion":respuesta}