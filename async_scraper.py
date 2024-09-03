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
            await page.wait_for_selector('h1')
            title = await page.locator('h1').text_content()
            print(f"Title: {title} from {url}")

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
