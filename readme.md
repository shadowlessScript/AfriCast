# What is Nairobi Cryer?
It is a content aggregator, built on Django and cleavages Requests and BeautifulSoup4 libraries for its web scraper algorithm, that aggregates news headlines and their respective links from different Kenyan news websites.

# Features
 - Aggregates news headlines from various Kenyan news websites.
 - Provides links to the original articles for more information.
 - Can aggregate specific categories such as politics, entertainment, sports, and business.

# How does it work?
Nairobi Cryer sends a get request to a website and then get its HTML.
The program looks for tags with news headlines such as article or div or h3 tags, after it extracts its text, news headline link and also its thumbnail(currently deactivated).
Once all the previously saved websites' info has been processed and collected, it's sent to Django views and then displayed in an HTML template.

## Future improvement
 - Complete the trending functionality, analysis of all the scraped data to find similarities.

# Installation
To install Nairobi Cryer follow these steps:
1. Clone the repo.
   ```commandline
   git clone https://github.com/shadowlessScript/AfriCast.git
   ```
2. Create a virtual environment inside the project folder.
    ```commandline
   python -m venv <env name>   
   ```
   - activate the virtual environment for CMD, (you use backslash or forward slash for Windows powershell)
     ```commandline
      .\<env name>\Scripts\activate
        ```
   - activate virtual environment for linux or git bash
     ```commandline
     source <env name>/Scripts/activate
     ```
3. Install the required libraries (from requirements.txt file found in the project folder)
    ```commandline
   pip install -r requirements.txt
    ```
4. Run project.
    ```commandline
    cd kenya_aggregator  
   ```
   ```commandline
   python manage.py runserver
   ```
# Author
[@shadowlessScript](https://github.com/shadowlessScript)

# License
[GNU license](LICENSE)