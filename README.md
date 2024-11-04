# Real Estate Listings Scraper and Report Generator

This Python script automates the process of scraping rental property listings from Trulia.com based on specified criteria, generates a PDF report of these listings, and emails the report to a specified email address.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Configuration](#configuration)
- [Detailed Explanation](#detailed-explanation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)


## Overview

The script performs the following tasks:

1. **Web Scraping**: Navigates to Trulia.com with predefined search criteria and extracts property listings.
2. **PDF Generation**: Compiles the extracted data into a neatly formatted PDF report.
3. **Email Dispatch**: Sends the PDF report to a specified email address using SMTP.

## Features

- Automated data extraction from Trulia.com.
- Dynamic PDF report generation.
- Email sending functionality with attachment support.
- Customizable search criteria and email settings.
- Error handling and logging for easy debugging.

## Prerequisites

- Python 3.6 or higher.
- Google Chrome browser installed.
- Basic knowledge of Python and command-line operations.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/real-estate-scraper.git
cd real-estate-scraper
```

### 2. Create a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

If a `requirements.txt` file is not provided, install the dependencies manually:

```bash
pip install os-sys smtplib time datetime python-dotenv reportlab beautifulsoup4 selenium webdriver-manager
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root directory and add your email credentials:

```env
EMAIL_USER=your_email@example.com
EMAIL_PASS=your_email_password
```

**Note**: For Gmail accounts, you may need to enable "Less secure app access" or use an App Password if 2FA is enabled.

### 5. Install ChromeDriver

The script uses `webdriver-manager` to automatically manage the ChromeDriver version, so you don't need to install it manually.

## Usage

Run the script using the following command:

```bash
python3 real_estate_scraper.py
```

Ensure that the script has execution permissions or run it directly with Python.

## Configuration

### Modifying Search Criteria

In the `main()` function, update the `url` variable to change the search parameters:

```python
url = 'https://www.trulia.com/for_rent/YourCity,YourState/YourCriteria/'
```

- **Location**: Replace `YourCity,YourState` with the desired location.
- **Criteria**: Adjust the URL to include specific search filters like number of beds, price range, etc.

### Email Settings

By default, the script sends the email to the address specified in `EMAIL_USER`. To change the recipient, modify the `to` parameter in the `send_email()` function call:

```python
send_email(
    subject='Weekly Real Estate Report',
    body='Please find the attached real estate report.',
    to='recipient_email@example.com',
    attachment_path=pdf_filename
)
```

### Running in Headless Mode

Set the `headless` option to `True` to run the browser in headless mode (without a GUI):

```python
options.headless = True
```

## Detailed Explanation

### 1. Web Scraping with Selenium and BeautifulSoup

- **Selenium WebDriver**: Automates Chrome to navigate to the specified URL.
- **Waiting for Elements**: Utilizes `WebDriverWait` and `expected_conditions` to wait for the property listings to load.
- **BeautifulSoup Parsing**: Parses the page source to extract property details like address, price, beds, baths, square footage, and links.

### 2. Generating the PDF Report

- **ReportLab**: Creates a PDF document with the extracted property details.
- **Formatting**: Includes headers, timestamps, and handles pagination if the content exceeds one page.

### 3. Sending the Email

- **EmailMessage**: Constructs the email with the subject, body, and attachment.
- **smtplib**: Connects to the SMTP server (Gmail in this case) to send the email.

## Troubleshooting

### Common Issues and Solutions

#### ChromeDriver Errors

If you encounter errors related to ChromeDriver:

- Ensure that Google Chrome is installed and up to date.
- The `webdriver-manager` should automatically handle the correct version, but if issues persist, install the matching ChromeDriver version manually.

#### Email Not Sending

- Double-check your email credentials in the `.env` file.
- For Gmail accounts:
  - Enable "Less secure app access" in your account settings.
  - If using 2FA, generate an App Password and use it in `EMAIL_PASS`.
- Ensure that your network allows outbound connections on port `587`.

#### No Properties Found

- The search criteria might be too restrictive. Try broadening your search parameters.
- Trulia's website structure may have changed. Inspect the page to update the `data-testid` selectors if necessary.

#### SSL Errors

If you receive SSL errors when connecting to the SMTP server:

- Verify that your system's date and time are correct.
- Update your Python installation to the latest version.

### Logging and Debugging

The script prints informative messages to the console. If an error occurs, it will display the traceback to help identify the issue.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.




**Disclaimer**: This script is intended for educational purposes. Scraping websites may violate their terms of service. Always check the website's policies before scraping and use responsibly.
