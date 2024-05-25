from fastapi import FastAPI
import pandas as pd


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

