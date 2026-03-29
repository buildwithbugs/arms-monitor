import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config import ARMS_URL, ARMS_USERID, ARMS_PASSWORD

MYCOURSE_URL = "https://arms.sse.saveetha.com/StudentPortal/MyCourse.aspx"


class ARMSScraper:
    def __init__(self):
        print("[✓] ARMSScraper ready")

    def _create_driver(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--log-level=3")
        options.add_argument("--disable-extensions")
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    def _login(self, driver):
        wait = WebDriverWait(driver, 20)
        try:
            print(f"[*] Logging in...")
            driver.get(ARMS_URL)
            time.sleep(3)
            wait.until(EC.presence_of_element_located((By.NAME, "txtusername"))).send_keys(ARMS_USERID)
            driver.find_element(By.NAME, "txtpassword").send_keys(ARMS_PASSWORD)
            driver.find_element(By.NAME, "btnlogin").click()
            time.sleep(4)
            print("[✓] Logged in successfully")
            return True
        except Exception as e:
            print(f"[✗] Login error: {e}")
            return False

    def _scrape_mycourse(self, driver):
        """Go directly to MyCourse page and scrape completed courses table"""
        results = []
        try:
            print(f"[*] Opening My Course page...")
            driver.get(MYCOURSE_URL)
            time.sleep(4)

            tables = driver.find_elements(By.TAG_NAME, "table")
            print(f"[*] Found {len(tables)} table(s) on My Course page")

            for table in tables:
                rows = table.find_elements(By.TAG_NAME, "tr")
                if len(rows) < 2:
                    continue

                headers = [th.text.strip().lower()
                           for th in rows[0].find_elements(By.XPATH, ".//th|.//td")]
                print(f"[*] Table headers: {headers}")

                # Match the Completed Courses table
                if "grade" not in " ".join(headers) or "course" not in " ".join(headers):
                    continue

                print(f"[✓] Completed Courses table found — {len(rows)-1} row(s)")
                for row in rows[1:]:
                    cells = [c.text.strip() for c in row.find_elements(By.TAG_NAME, "td")]
                    if len(cells) < 4 or not cells[1]:
                        continue
                    results.append({
                        "sno":         cells[0] if len(cells) > 0 else "",
                        "course_code": cells[1] if len(cells) > 1 else "",
                        "course_name": cells[2] if len(cells) > 2 else "",
                        "grade":       cells[3] if len(cells) > 3 else "N/A",
                        "status":      cells[4] if len(cells) > 4 else "N/A",
                        "month_year":  cells[5] if len(cells) > 5 else "N/A",
                    })
                break

        except Exception as e:
            print(f"[✗] Scrape error: {e}")

        return results

    def scrape_results(self):
        driver = None
        try:
            driver = self._create_driver()
            if not self._login(driver):
                return None
            results = self._scrape_mycourse(driver)
            print(f"[✓] Found {len(results)} completed course(s)")
            return results
        except Exception as e:
            print(f"[✗] Scrape error: {e}")
            return None
        finally:
            if driver:
                try:
                    driver.quit()
                    print("[✓] Browser closed")
                except Exception:
                    pass

    def close(self):
        pass