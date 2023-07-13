# JioSaavn and Wynk Music Scraper
This Python script allows you to scrape song data from JioSaavn and Wynk Music platforms. It retrieves information such as song name, duration, play count, album, year, artist, label, language, and more. The script uses the BeautifulSoup library to parse the HTML content and the Requests library to send HTTP requests.

## Prerequisites
Make sure you have the following libraries installed:
* requests
* pandas
* numpy
* BeautifulSoup
* requests_futures

### If any of these packages are not installed, the script will attempt to install them automatically.

## Usage
1. Download the python script directly.

2. Open the terminal or command prompt and navigate to the directory where the script is located.

3. Run the following command to execute the script:
python jio-wynk-scrapper.py

4. You will be prompted to enter a number corresponding to the type of data you want to scrape:
![Screenshot (12)](https://github.com/aceisreal/jio-wynk-scrapper/assets/42153415/d03ef511-452b-423a-8192-a845f0a98375)

5. Depending on your input, you may be asked to provide additional information such as a playlist URL or album URL.

6. The script will start scraping the song data from the selected source. The progress will be displayed on the console.

7. Once the scraping is complete, the script will close and save the data to a CSV file named (userinput)_(date-time).CSV, where userinput represents the input you gave at the start and (date-time) represents the current date and time. The CSV will be saved on your desktop.

### Note: If the script is unresponsive or stuck then close the script and reopen it again.

## Output
The script generates a CSV file containing the scraped song data. The CSV file includes the following columns:

* Song Title
* Song Length
* Song PlayCount
* Song Album
* Song Year
* Song Artist
* Song Label
* Song Language

### Note: The column names may vary depending on the selected source and the available data.

## Limitations
* This script relies on the structure and API endpoints of the JioSaavn and Wynk Music websites. Any changes to these websites may break the script.
* The script assumes a stable internet connection. If there are connection errors, it will display an appropriate error message.
* The script may not handle all possible edge cases or exceptions. It is recommended to handle exceptions and error conditions based on your particular use case.


## Disclaimer
This script is for educational purposes only. The scraping of data from websites may be subject to legal restrictions or terms of service. Use this script responsibly and in accordance with the applicable laws and regulations. The author does not take any responsibility for the misuse of this script.

## MIT License

Copyright (c) 2023 Ajit Prahlad

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
