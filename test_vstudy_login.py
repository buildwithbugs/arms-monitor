from vstudy_scraper import VStudyScraper


def main():
    scraper = VStudyScraper()
    success = False

    try:
        print("[*] Starting dedicated VStudy Chrome profile...")
        scraper._create_driver()

        print("[*] Authenticating and opening profile...")
        courses = scraper.scrape_course_results(scraper.driver)

        if not courses:
            print("[✓] No course data found on the profile page")
            return

        print(f"[✓] Found {len(courses)} course(s)")
        for item in courses[:3]:
            print(item)
        success = True

    except Exception as exc:
        print(f"[✗] VStudy test error: {exc}")
    finally:
        scraper.close()
        print("[*] Browser closed.")

    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())