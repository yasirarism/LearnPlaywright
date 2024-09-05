import uvicorn
import os

port = os.environ.get("PORT", 80)

if __name__ == "__main__":
    uvicorn.run("async_scraper:app", host="0.0.0.0", port=int(port), reload=False)