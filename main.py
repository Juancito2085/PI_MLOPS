from fastapi import FastAPI


app = FastAPI()

@app.get("/developer_reviews_analysis/{desarrollador}",description="Es una prubea")
async def developer_reviews_analysis( desarrollador : str ):
    return {"valve" : desarrollador*2}

