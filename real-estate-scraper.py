#!/usr/bin/env python3

import os
import sys
import smtplib
import time
from email.message import EmailMessage
from datetime import datetime
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load environment variables from a .env file if present
load_dotenv()

# Email credentials from environment variables
EMAIL_ADDRESS = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASS')

def scan_website(url):
    """
    Scans the given website URL using Selenium and returns a list of property data.
    """
    import traceback
    options = Options()
    options.headless = False  # Set to True after testing
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-webgl')
    options.add_argument('--log-level=3')
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/86.0.4240.183 Safari/537.36'
    )

    driver = None

    try:
        print("Launching Chrome browser...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        print("Navigating to URL:", url)
        driver.get(url)

        print("Current URL:", driver.current_url)
        print("Page Title:", driver.title)

        print("Waiting for listings to load...")
        # Wait for the property cards to load using the data-testid attribute
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="home-card-rent"]'))
        )
        print("Listings loaded.")

        # Scroll down to load more listings if necessary
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for new listings to load

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find all property cards
        listings = soup.find_all('div', {'data-testid': 'home-card-rent'})

        print(f"Found {len(listings)} listings.")

        properties = []

        for listing in listings:
            try:
                # Extract details using data-testid attributes
                address_div = listing.find('div', {'data-testid': 'property-address'})
                address = address_div.get_text(separator=' ', strip=True) if address_div else 'N/A'

                price_div = listing.find('div', {'data-testid': 'property-price'})
                price = price_div.get_text(strip=True) if price_div else 'N/A'

                beds_div = listing.find('div', {'data-testid': 'property-beds'})
                beds = beds_div.get_text(strip=True) if beds_div else 'N/A'

                baths_div = listing.find('div', {'data-testid': 'property-baths'})
                baths = baths_div.get_text(strip=True) if baths_div else 'N/A'

                sqft_div = listing.find('div', {'data-testid': 'property-floorSpace'})
                sqft = sqft_div.get_text(strip=True) if sqft_div else 'N/A'

                link_tag = listing.find('a', {'data-testid': 'property-card-link'})
                link = 'https://www.trulia.com' + link_tag['href'] if link_tag else 'N/A'

                properties.append({
                    'Address': address,
                    'Price': price,
                    'Beds': beds,
                    'Baths': baths,
                    'SqFt': sqft,
                    'Link': link
                })
            except Exception as e:
                print(f"Error parsing listing: {e}")
                continue

        return {'status': 200, 'properties': properties, 'url': url}
    except Exception as e:
        print("An error occurred:", e)
        traceback.print_exc()
        return {'error': str(e), 'url': url}
    finally:
        if driver:
            driver.quit()

def generate_pdf(properties, filename):
    """
    Generates a PDF report from the list of properties.
    """
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    c.setTitle("Weekly Real Estate Report")

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Weekly Real Estate Report")

    # Date
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 70, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    y_position = height - 100

    for prop in properties:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y_position, f"Address: {prop['Address']}")
        y_position -= 15

        c.setFont("Helvetica", 12)
        c.drawString(50, y_position, f"Price: {prop['Price']}")
        y_position -= 15

        c.drawString(50, y_position, f"Beds: {prop['Beds']}")
        y_position -= 15

        c.drawString(50, y_position, f"Baths: {prop['Baths']}")
        y_position -= 15

        c.drawString(50, y_position, f"SqFt: {prop['SqFt']}")
        y_position -= 15

        c.drawString(50, y_position, f"Link: {prop['Link']}")
        y_position -= 25  # Extra space between listings

        if y_position < 100:
            c.showPage()
            y_position = height - 50

    c.save()

def send_email(subject, body, to, attachment_path):
    """
    Sends an email with the specified subject, body, and attachment to the recipient.
    """
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to

    # Read the properties to include in the email body
    with open(attachment_path, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(f.name)

    msg.set_content(body)

    # Attach PDF
    msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)

    # Send the email via SMTP server
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")
        sys.exit(1)

def main():
    # Construct the URL with search parameters
    url = 'https://www.trulia.com/for_rent/Palestine,TX/2p_beds/2000-2500_sqft/'

    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("Email credentials are not set. Please set EMAIL_USER and EMAIL_PASS environment variables.")
        sys.exit(1)

    # Scan the website
    result = scan_website(url)

    if 'error' in result:
        print(f"Error scanning website: {result['error']}")
        sys.exit(1)

    properties = result['properties']

    if not properties:
        print("No properties found matching the criteria.")
        sys.exit(0)

    # Generate PDF report
    pdf_filename = 'weekly_real_estate_report.pdf'
    generate_pdf(properties, pdf_filename)
    print(f"PDF report generated: {pdf_filename}")

    # Send the report via email
    send_email(
        subject='Weekly Real Estate Report',
        body='Please find the attached weekly real estate report.',
        to=EMAIL_ADDRESS,
        attachment_path=pdf_filename
    )

if __name__ == "__main__":
    main()
