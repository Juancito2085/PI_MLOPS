from fastapi import FastAPI
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


#Funcion de recomendacion de juegos

def similitud(id):
    df=pd.read_parquet("Datasets/data.parquet")
    if df[df['id']==id].empty:
        return "El juego no se encuentra en la base de datos"
    df.reset_index(drop=True, inplace=True)

    #Vectorizar el nombre de los productos
    vectorizer=TfidfVectorizer()
    tfidf_matrix=vectorizer.fit_transform(df[['app_name','genres','tags']].apply(lambda x: ' '.join(x),axis=1))

    #Calcular la matriz de similitud del coseno
    similarity_matrix=cosine_similarity(tfidf_matrix)

    #Obtener el indice del producto dado
    producto_index=df[df['id']==id].index[0]
    
    #Obtener los indices de los productos más similares
    product_similarities=similarity_matrix[producto_index]

    #Obtener los nombres de los 5 productos más similares 
    most_similar_products_index=np.argsort(-product_similarities)[1:6]

    #Obtener los nombres de los productos
    most_similar_products=df.loc[most_similar_products_index,'app_name']
    return most_similar_products

#Creacion de la API
app = FastAPI()

@app.get("/")
async def root():
    return {"Message": "PI MLOPS"}

@app.get("/developer/",description="Devuelve el nombre del desarrollador y la cantidad de items por año y la proporción de items gratis")
async def developer( desarrollador : str = "Valve"):
    #Se normaliza la entrada
    desarrollador=desarrollador.title()
    #Se carga el dataset
    df_developers=pd.read_parquet(r'Datasets/developers.parquet')
    #Se verifica si el desarrollador existe con esta estructura de control
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
        del df_developers
        return{desarrollador:data}
    else:
        return{'No existe el desarrollador '+ desarrollador}

@app.get("/userdata/",description="Devuelve el nombre del usuario, el dinero gastado, el porcentaje de recomendaciones y la cantidad de items")
async def userdata( user_id : str = "maplemage"):
    #Se cargan los datasets
    df_users=pd.read_parquet(r'Datasets/users.parquet')
    df_recc=pd.read_parquet(r'Datasets/user_recommends.parquet')
    #Se verifica si el usuario existe
    if user_id in df_users['user_id'].values:
        df_users=df_users[df_users['user_id']==user_id]
        cantidad_juegos=df_users['items_count'].values[0]
        dinero_gastado=df_users['price'].sum().round()
        if user_id in df_recc['user_id'].values:
            recomendaciones = str(df_recc[df_recc['user_id']==user_id]['perc_recomm'].iloc[0])
        else:
            recomendaciones = "0%"
            del df_recc
            del df_users
        return {'Usuario':user_id,'Dinero gastado':dinero_gastado,'Recomendaciones':recomendaciones,'Cantidad de juegos':int(cantidad_juegos)}
    else:
        return{'No existe el usuario'+ user_id}

@app.get("/UserForGenre/",description="Devuelve el usuario que más horas acumula jugadas para el género dado y una lista de la cantidad de horas jugadas por año")
async def UserForGenre( genero : str = "Action"):
    #Se cargan los datasets
    df_users=pd.read_parquet(r'Datasets/users.parquet')
    #Se normaliza la entrada
    genero=genero.title()
    #Se verifica si el genero existe
    if genero in df_users['genres'].values:
        df_users=df_users[df_users['genres']==genero]
        df_users.drop(columns=['items_count','price','genres'],inplace=True)
        usuario=df_users.groupby('user_id')['playtime_forever'].sum().idxmax()
        df_users=df_users[df_users['user_id']==usuario]
        horas_jugadas = [{'Año': row['release_year'], 'Horas': row['playtime_forever']} for index, row in df_users.iterrows()]
        respuesta={'Usuario con mas horas jugadas para el genero '+ genero:usuario,'Horas jugadas':horas_jugadas}
        del df_users
        return respuesta
    else:
        return {'No existe el genero ' + genero}

@app.get("/best_developer_year/",description="Devuelve el top 3 de desarrolladores con juegos más recomendados por usuarios para el año dado.")
async def best_developer_year( anio : int = 2015):
    #Se carga el dataset
    df_developers=pd.read_parquet(r'Datasets/developers.parquet')
    #Se verifica si el año existe
    if anio in df_developers['release_year'].values:
        #Se hace una reducción del dataset
        df_developers=df_developers[df_developers['release_year']==anio]
        df_developers.drop(columns=['price','item_id','Negative','Neutral','Positive','False','release_year'],axis=1,inplace=True)
        #Se agrupan los datos por desarrollador
        df_developers=df_developers.groupby('developer')['True'].sum()
        df_developers=df_developers.sort_values(ascending=False)
        respuesta=[{'Puesto '+str(i+1):df_developers.index[i]} for i in range(3)]
        del df_developers
        return{'Top3':respuesta}
    else:
        return{'Año ' +str(anio)+' no encontrado'}

@app.get("/developer_reviews_analysis/",description="Devuelve el nombre del desarrollador y la cantidad de reviews positivas y negativas")
async def developer_reviews_analysis( desarrollador : str ="Valve" ):
    #Se normaliza la entrada
    desarrollador=desarrollador.title()
    #Se carga el dataset
    df=pd.read_parquet("Datasets/developers.parquet")
    if desarrollador not in df["developer"].values:
        return {"respuesta" : "Desarrollador no encontrado"}
    else:
        respuesta=df[df['developer']==desarrollador][['Positive','Negative']].sum()
        del df
        return {desarrollador : respuesta.to_dict()}

@app.get("/recomendacion_juego/",description="Devuelve una lista con 5 juegos similares al juego ingresado")
async def recomendacion_juego( id_producto : int = 508290 ):
    #Se invoca a la función de remcomendación
    respuesta=similitud(id_producto)
    respuesta=respuesta.tolist()
   
    return {"Juegos recomendados":respuesta}