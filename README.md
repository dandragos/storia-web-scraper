# Storia Web Scraper

## Overview
This is a Python web scraper designed to extract rental property listings from the Storia website. The program allows users to specify search criteria such as city, minimum and maximum price range, and the number of rooms. It then scrapes the Storia website for relevant listings, extracts key information, and exports the data to an Excel file. Additionally, the program sorts the listings based on price per area before displaying and exporting the results.

## Requirements
- Python 3
- Requests library
- BeautifulSoup library
- Pandas library

## You can install the required libraries using the following command:

*pip install requests beautifulsoup4 pandas*


## How it Works
### Initialization:

The program begins by importing the necessary libraries: requests for making HTTP requests, BeautifulSoup for parsing HTML, and pandas for handling data.
Regular expressions (re module) are used to define patterns for extracting price, number of rooms, and area information from the HTML content.

### Scraping Function:

The scrape_storia function is the core of the program. It takes user-defined parameters such as city, minimum price, maximum price, and number of rooms.
The function iterates through multiple pages of search results, extracting details like title, price, number of rooms, area, and link for each listing.
Listings are stored in a list of dictionaries.

### Data Processing:

The program calculates the price per area for each listing and stores the results in a pandas DataFrame.
The listings are sorted based on price per area in ascending order.

### User Interaction:

The main function prompts the user for input, allowing them to specify the city, sector (for Bucharest), and additional filters such as price range and number of rooms.

### Export to Excel:

The program exports the sorted listings to an Excel file with a filename based on the selected filters.

### Display Results:

The program prints the details of each listing, including title, price, number of rooms, area, price per area, and a link.

### End of Execution:

The user is informed about the successful export of data to the Excel file.

## How to Use:

1) Run the script.
2) Provide the requested information regarding the city, sector (for Bucharest), and filters.
3) The program will scrape Storia for listings based on the provided criteria.
4) Results will be displayed, and the data will be exported to an Excel file.

*Note: Please use this script responsibly and in compliance with the terms of use of the target website. (It was made for personal use)*

*Made by Dan Dragos*
