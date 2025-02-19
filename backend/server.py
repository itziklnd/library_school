from fastapi import FastAPI
from database import search_books, add_book

app = FastAPI()

@app.get("/search")
def search(query: str):
    results = search_books(query)
    return [{"title": title, "author": author} for title, author in results]

@app.post("/add")
def add(title: str, author: str):
    add_book(title, author)
    return {"message": "📚 ספר נוסף בהצלחה!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
