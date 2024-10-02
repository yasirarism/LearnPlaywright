import asyncio, re
from urllib.parse import urlparse, unquote
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
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")

    async with webdriver.Chrome(options=options) as driver:
        await driver.get(url, wait_load=True)
        await asyncio.sleep(0.5)

        # some random mouse-movements over iframes
        pointer = driver.current_pointer
        await pointer.move_to(500, 200, smooth_soft=60, total_time=0.5)
        await pointer.move_to(20, 50, smooth_soft=60, total_time=0.5)
        await pointer.move_to(8, 45, smooth_soft=60, total_time=0.5)
        await pointer.move_to(500, 200, smooth_soft=60, total_time=0.5)
        await pointer.move_to(166, 206, smooth_soft=60, total_time=0.5)
        await pointer.move_to(200, 205, smooth_soft=60, total_time=0.5)

        iframes = await driver.find_elements(By.TAG_NAME, "iframe")
        await asyncio.sleep(0.5)

        iframe_document = None
        for iframe in iframes:
            # filter out correct iframe document
            iframe_document = await iframe.content_document
            try:
                checkbox = await iframe_document.find_element(By.CSS_SELECTOR,
                                                              "#JStsl2 > div > label > input[type=checkbox]",
                                                              timeout=5)
            except NoSuchElementException:
                pass
            else:
                await checkbox.click(move_to=True)
                await asyncio.sleep(1)

        scripts = await driver.find_elements(By.TAG_NAME, 'script')
        for script in scripts:
            script_text = await script.get_attribute('textContent')
            match = re.search(r'window\.open\("([^"]+)"\)', script_text)
            if match:
                return match.group(1)
        else:
            print("Captcha failed, retrying")
            await driver.refresh()
            await asyncio.sleep(30)
