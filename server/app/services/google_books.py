import httpx

BASE_URL = "https://www.googleapis.com/books/v1/volumes"
RECENT_SEARCHES = []

def add_to_recent_searches(query: str):
    global RECENT_SEARCHES
    RECENT_SEARCHES.append(query)
    # Limit the size to the last 10 searches
    RECENT_SEARCHES = RECENT_SEARCHES[-10:]

async def search_google_books(query: str):
    add_to_recent_searches(query)
    params = {"q": query}
    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params)
        data = response.json()

        if not data.get("items"):
            return {"message": "No books found for the given query."}

        books = data.get("items", [])
        processed_books = []
        for book in books:
            volume_info = book.get("volumeInfo", {})
            title = volume_info.get("title", "N/A")
            authors = volume_info.get("authors", ["Unknown"])
            description = volume_info.get("description", "No description available.")
            thumbnail = volume_info.get("imageLinks", {}).get("thumbnail", None)

            processed_books.append({
                "title": title,
                "authors": authors,
                "description": description,
                "thumbnail": thumbnail
            })

        return processed_books
