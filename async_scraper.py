import asyncio, re
from urllib.parse import urlparse, unquote
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from typing import Union, Tuple

app = FastAPI(
    title="YasirPedia Api",
    description="Useful Rest Api Build Using FastAPI By YasirPedia 🚀",
    version="0.2.0",
    contact={
        "name": "Yasir Aris M",
        "url": "https://github.com/YasirArisM",
        "email": "yasiramunandar@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    docs_url="/docs",
    openapi_url="/openapi.json",
    redoc_url="/redocs",
)

@app.get("/dood", summary="Scrape DDL From Dood", tags=["Drama & Film"])
async def scrape_dood(url: Union[str, None]):
    if not url:
        raise HTTPException(status_code=404, detail="Missing url")
    
    if '/d/' in url:
        url = url.replace('/d/', '/e/')
    
    domain = urlparse(url).netloc

    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)  # Launch Chromium in headless mode
        context = await browser.new_context()
        # Set custom user-agent and referer headers
        await context.set_extra_http_headers({
            "Referer": f"https://{domain}/",
            "User-Agent": "Mozilla/5.0 (Linux; Android 15; Pixel 9 Pro Fold Build/AP3A.241005.015; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/129.0.6668.100 Mobile Safari/537.36"
        })
        page = await context.new_page()

        try:
            await page.goto(url)
            await page.wait_for_timeout(5000)  # Wait for the page to load

            # Extract the video URL
            try:
                video_element = await page.query_selector("video")
                video_url = await video_element.get_attribute("src") if video_element else None
            except Exception as e:
                raise HTTPException(status_code=404, detail={"error": "Video URL not found", "message": str(e)})

            video_title = await page.title()

            if video_url:
                return {
                    "success": True,
                    "video_url": video_url,
                    "referer": domain,
                    "title": video_title
                }
            else:
                raise HTTPException(status_code=404, detail="Video URL not found")

        except Exception as e:
            raise HTTPException(status_code=500, detail={"error": "Error fetching the page", "message": str(e)})
        finally:
            await browser.close()
