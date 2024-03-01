from django import template
import re

register = template.Library()


@register.filter(name="extract_domain_name")
def extract_domain_name(url):
    # Regular expression pattern to extract domain name
    pattern = r'https?://(?:www\.)?([a-zA-Z0-9-]+(?:\.[a-zA-Z]+)+)'
    match = re.match(pattern, url)
    if match:
        domain = match.group(1)
        # Split the domain name by dots and extract the first part
        domain_parts = domain.split('.')
        if len(domain_parts) > 1:
            domain = domain_parts[0]  # Extracting the second-to-last part
            if domain == "nation":
                domain = "nation Africa"
        return domain.capitalize()
    else:
        return None
