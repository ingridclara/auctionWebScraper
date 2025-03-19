# auctionWebScraper

## Scope
Create a web scraper that monitors an [auction site](https://www.dupagesheriff.org/foreclosureListings), extracts JSON data, checks for prices on listings, and performs two actions if a price is found.
1. Sends an alert email to a T-Mobile phone number via Amazon SES.
2. Saves the listing information to a DynamoDB table.

## Components
AWS Lambda - Runs the scraper code once daily.
Amazon SES - Sends email notifications.
DynamoDB - Stores listing data.
JSON Processing - Extracts and verifies prices from the auction site's JSON.
This is the site the prices are usually listed the day before the sale
