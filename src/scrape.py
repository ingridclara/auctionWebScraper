#####################################################
#                                                   
#                     handler                        
# 
#####################################################

# Import required modules
import requests # allows you to send HTTP requests using Python
import json 
import boto3 

# Define global variables
foreclosuresUrl = 'https://myocv.s3.amazonaws.com/ocvapps/a36160187/foreclosureListings.json'


def handler(event, context):
    scrape(foreclosuresUrl)



#####################################################
#                                                   
#                     scrape                        
# 
#####################################################


# Create function to collect data utilizing web scraping
def scrape(url):

    # request data from html
    response = requests.get(url) 

    data_string = response.text
    json_data = json.loads(data_string) # Parse the JSON string

    # LOOP THROUGH EACH LIST 
    for item in json_data:
        opening_bid = item['bid']
        sale_date = item['dayOfSale']
        property_address = item['propertyAddress']
        if opening_bid != 'Not Provided':
            print("\nOpening Bid:")
            print(opening_bid)
            print("\nDay of Sale:")
            print(sale_date)
            print("\nProperty Address:")
            print(property_address)
            
            storeDataToDynamo(property_address, opening_bid, sale_date)

            textAlert(property_address, sale_date, opening_bid)




#####################################################
#                                                   
#                storeDataToDynamo                        
# 
#####################################################


def storeDataToDynamo(property_address,opening_bid,sale_date):
    print("Attempting to insert listing in Dynamo")
    try:
        dynamodb = boto3.client('dynamodb')
        dynamodb.put_item(TableName='auction_listings', Item={'property_address':{'S':property_address},'opening_bid':{'S':opening_bid},'sale_date':{'S':sale_date}})

    except ClientError as e:
        # Extract error code and message
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        print(f"Error: {error_code}: {error_message}")
    except BotoCoreError as e:
        print(f"Botocore Error: {e}")


#####################################################
#                                                   
#                textAlert                        
# 
#####################################################


def textAlert(property_address, opening_bid, sale_date):
    message=f"Auction found! Property Address is {property_address} starting at {opening_bid} on {sale_date}"
    client = boto3.client('sns')
    response = client.publish(
        TargetArn='arn:aws:sns:us-east-1:654654149547:AuctionListing',
        Message= message,
        MessageStructure='string'
        )
