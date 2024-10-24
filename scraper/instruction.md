# Ecommerce shop scraper

*Below scraper is meant to be used with provided configuration.*  

This scraper allows to scrape given electronic shop, including:
- Categories
- Subcategories
- Products
- Photos

## Using scraper

1. Navigate to directory where the scraper is *(for default config)*:   
`cd scraper`
2. Install scraper dependencies ***(remember to activate venv)***:  
`pip install -r requirements.txt`
3. Execute scraper script:  
`python scraper.py`
4. All scraped resources will be in `output/output.json`
5. All scraped images will be in `output/images` directory

## Package contents
- `example_schema.json` - exemplary json schema of the scraper output
- `README.md` - scraper instruction
- `requriements.txt` - scraper dependencies
- `scraper.py` - scraper script
- `.gitignore` - module's **.gitignore** file