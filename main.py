from fastapi import FastAPI


app = FastAPI()

@app.get("/developer_reviews_analysis/{desarrolladora}",description="Es una prubea")
async def developer_reviews_analysis( desarrolladora : str ):
    return {"valve" : {"Negative" : 182, "Neutral" : 120, "Positive" : 278}}