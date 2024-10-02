import asyncio
from urllib.parse import urlparse, unquote
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
from fastapi import FastAPI, HTTPException
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
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)  # Use chromium or the browser of choice
        page = await browser.new_page()
        await page.goto(url)
        await asyncio.sleep(0.5)

        # Random mouse movements
        await page.mouse.move(500, 200, steps=60)
        await page.mouse.move(20, 50, steps=60)
        await page.mouse.move(8, 45, steps=60)
        await page.mouse.move(500, 200, steps=60)
        await page.mouse.move(166, 206, steps=60)
        await page.mouse.move(200, 205, steps=60)

        # Handle iframes
        iframe_document = None
        iframes = page.frames
        await asyncio.sleep(0.5)

        for iframe in iframes:
            try:
                checkbox = await iframe.query_selector(
                    "#JStsl2 > div > label > input[type=checkbox]"
                )
                if checkbox:
                    await checkbox.click()
                    await asyncio.sleep(1)
                    break  # Exit once we find and click the checkbox
            except PlaywrightTimeoutError:
                pass

        # Find script with window.open() and extract the URL
        scripts = await page.locator('script').all()
        for script in scripts:
            script_text = await script.text_content()
            if script_text:
                match = re.search(r'window\.open\("([^"]+)"\)', script_text)
                if match:
                    print(match.group(1))
                    await browser.close()
                    return
        else:
            print("Captcha failed, retrying")
            await page.reload()
            await asyncio.sleep(30)

        await browser.close()
    
