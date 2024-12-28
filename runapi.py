import uvicorn
import os

port = os.environ.get("PORT", 8081)

if __name__ == "__main__":
    uvicorn.run("async_scraper:dood_app", host="0.0.0.0", port=int(port), reload=False)
