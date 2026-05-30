from playwright.sync_api import sync_playwright

def run_cuj(page):
    page.goto("http://localhost:5000")
    page.wait_for_timeout(1000)

    # Login
    page.get_by_label("Username").fill("admin")
    page.get_by_label("Password").fill("admin123")
    page.get_by_role("button", name="Authenticate Session").click()
    page.wait_for_timeout(2000)

    # Dashboard check
    page.screenshot(path="/home/jules/verification/screenshots/dashboard.png")
    page.wait_for_timeout(1000)

    # Settings check
    page.goto("http://localhost:5000/settings")
    page.wait_for_timeout(1000)
    page.screenshot(path="/home/jules/verification/screenshots/settings.png")
    page.wait_for_timeout(1000)

    # Batch detail check
    page.goto("http://localhost:5000/batches/VAC-MRNA-99")
    page.wait_for_timeout(2000)
    page.screenshot(path="/home/jules/verification/screenshots/batch.png")
    page.wait_for_timeout(2000)

    # Timeline check
    page.goto("http://localhost:5000/timeline")
    page.wait_for_timeout(1000)
    page.screenshot(path="/home/jules/verification/screenshots/timeline.png")
    page.wait_for_timeout(1000)


if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos",
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
