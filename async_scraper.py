import asyncio
from urllib.parse import urlparse, unquote
from playwright.async_api import async_playwright
from fastapi import FastAPI, HTTPException
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
        # Launch a headless browser
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(java_script_enabled=True)
        domain = urlparse(url)
        try:
            # Navigate to the URL
            await page.goto(url, timeout=60000, wait_until='domcontentloaded')

            # Wait for the element to be present and extract text
            # await page.wait_for_selector('h1')
            # title = await page.locator('h1').text_content()
            await page.wait_for_selector("a[href='#download_now']")
            # Click the button
            # await page.click("a[href='#download_now']")
            # await page.wait_for_timeout(6000)
            # await page.click("small.___siz_fol.d-block")
            res = await page.get_attribute("a.btn.btn-primary.d-flex.align-items-center.justify-content-between", "href")
            await page.goto(domain.scheme + "://" + domain.netloc + str(res), timeout=60000, wait_until='domcontentloaded')
            ddl = await page.locator('a.btn.btn-primary').get_attribute('href')
            await browser.close()
            if ddl is None:
                return False, None, None
            name = unquote(urlparse(ddl).path.split("/")[-1])
            return {"status": True, "name": name, "url": ddl, "msg": "heee"}
            # parsed_url = urlparse(url)
            # await page.goto(f"{parsed_url.scheme}://{parsed_url.netloc}{res}")
            # print(await page.content())
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            await browser.close()
            raise HTTPException(status_code=404, detail="Element not found or href attribute missing.")
    
