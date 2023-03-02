import requests
from bs4 import BeautifulSoup
import concurrent.futures

url = "https://www.example.com" # Replace with the URL of the website to search
wordlist_file = "directory_wordlist.txt" # Replace with the path to your wordlist file
output_file = "directory_results.txt" # Replace with the path to the output file
max_workers = 10 # Maximum number of threads to use for multithreading

# Read the directory wordlist from file
with open(wordlist_file, "r") as f:
    directory_wordlist = [line.strip() for line in f]

# Open the output file for writing
with open(output_file, "w") as f:
    # Define a function for scraping a single directory
    def scrape_directory(directory):
        # Construct the URL for the directory
        directory_url = url + "/" + directory
        
        # Send a request to the directory URL
        response = requests.get(directory_url)
        
        # Check if the response status code indicates a successful connection
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Search for any links or keywords that indicate a directory website
            directory_links = soup.find_all('a', href=lambda href: href and ('directory' in href or 'listings' in href))
            
            # Construct the output result
            if directory_links:
                result = f"Directory website found at {directory_url}:\n"
                for link in directory_links:
                    result += f"{link['href']}\n"
            else:
                result = f"No directory website found at {directory_url}\n"
        else:
            result = f"Failed to connect to {directory_url}. Response code: {response.status_code}\n"
        
        # Write the output result to the output file
        f.write(result)
        return result

    # Use multithreading to scrape directories
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit tasks for each directory
        tasks = [executor.submit(scrape_directory, directory) for directory in directory_wordlist]
        
        # Wait for tasks to complete and print any exceptions
        for future in concurrent.futures.as_completed(tasks):
            try:
                result = future.result()
            except Exception as e:
                result = f"Exception: {str(e)}\n"
            print(result, end='')
