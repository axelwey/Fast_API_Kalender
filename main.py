from fastapi import FastAPI

app = FastAPI()
data=[
        {"titel":"dokter",
         "jaar":"2000",
         "maand":"july",
         "dag":"8"},
        {"titel":"school",
         "jaar":"2000",
         "maand":"july",
         "dag":"8"},
        {"titel":"werk",
         "jaar":"2000",
         "maand":"july",
         "dag":"8"}
     ]


@app.get("/")
async def root():
    return data