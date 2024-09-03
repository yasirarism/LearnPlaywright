import asyncio
from playwright.async_api import async_playwright

# Define a function to scrape data asynchronously using Playwright
async def scrape(url):
    async with async_playwright() as p:
        # Launch a headless browser
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            # Navigate to the URL
            await page.goto(url)

            # Wait for the element to be present and extract text
            # await page.wait_for_selector('h1')
            # title = await page.locator('h1').text_content()
            await page.wait_for_selector("a[href='#download_now']")
            # Click the button
            await page.click("a[href='#download_now']")
            # Optionally wait for some action after the click
            # await page.wait_for_timeout(6000)
            await page.wait_for_selector("small.___siz_fol.d-block")
            await page.click("small.___siz_fol.d-block")
            print(await page.content())
            # print(await page.get_attribute("a.btn.btn-primary.d-flex.align-items-center.justify-content-between", "href"))
            # print(await page.content())

        except Exception as e:
            print(f"Error scraping {url}: {e}")
        finally:
            await browser.close()

# Define the main function to handle multiple URLs
async def main():
    urls = [
        "https://dood.li/d/3trsd35zs445",
        "https://dood.li/d/ec9hwdrqpfoi",
    ]

    # Create a list of tasks for each URL
    tasks = [scrape(url) for url in urls]

    # Run all tasks concurrently
    await asyncio.gather(*tasks)

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
