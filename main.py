from fastapi import FastAPI
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

#Funcion para los json
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

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

@app.get("/developer/{desarrollador}",description="Devuelve un diccionario con el nombre del desarrollador y la cantidad de items por año y la proporción de items gratis")
async def developer( desarrollador : str ):
    desarrollador=desarrollador.title()
    df_developers=pd.read_parquet(r'Datasets/developers.parquet')
    if desarrollador in df_developers['developer'].values:
        df_developers=df_developers[df_developers['developer']==desarrollador]
        #Se eliminan las columnas que no se van a utilizar
        df_developers.drop(columns=['Negative','Neutral','Positive','True','False','developer'],inplace=True)
        #Total de items por cada año
        total = df_developers.groupby('release_year')['price'].count()
        #Cuenta la cantidad de items que no son gratis
        no_ceros = df_developers[df_developers['price'] != 0].groupby('release_year')['price'].count()
        no_ceros= no_ceros.reindex(total.index, fill_value=0)
        #Calacula la proporción de items gratis
        proporcion_gratis =round((1- no_ceros / total)*100,2)
        proporcion_gratis=proporcion_gratis.astype('str')+'%'
        #Doy formato a la respuesta
        data = [{'Año': int(year), 'Cantidad de items': int(total[year]), 'Contenido free': proporcion_gratis[year]} for year in total.index]
        return{desarrollador:data}
    else:
        return{'No existe el desarrollador '+ desarrollador}


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