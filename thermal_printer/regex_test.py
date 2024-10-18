import re

if __name__ == '__main__':
    # Adjust pattern to capture product name and price separately
    PRODUCT_PATTERN = r'^([\w\s]+)\s+(\d{1,3}\.\d{2})$'

    result = re.search(PRODUCT_PATTERN, 'Product  123            10.00')

    if result:
        product_name = result.group(1).strip()  # First group is the product name
        price = result.group(2)  # Second group is the price

        print(f'Product Name: "{product_name}", Price: {price}')
    else:
        print('No match found')
