from playwright.sync_api import sync_playwright

url = "https://chaldal.com/aci-pure-nazirshail-rice-5-kg"
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    page.goto(url, timeout=60000, wait_until="domcontentloaded")
    try:
        page.wait_for_selector("text=Nazirshail", timeout=30000)
    except Exception:
        print("Product text did NOT appear")
    page.wait_for_timeout(3000)
    print("URL:", page.url)
    page.screenshot(path="debug.png")
    text = page.inner_text("body")
    browser.close()

lines = [l for l in text.split("\n") if l.strip()]
print("Total lines:", len(lines))
for i in range(33, 41):
    print(i, ascii(lines[i]))