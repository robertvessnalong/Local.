# Local.

### A web application that allows users to find local restaurants, review restaurants, and favorite restaurant and reviews. Built using Python, Flask, JavaScript. Restaurant Data obtained from the Yelp API.

Note: This project is currently being constantly edited and considered not a final project.

### How to Use:

- To use this application, you will need to install the requirements.txt file.
- With that, you will also need a IPStack API Key and Yelp API Key.
- The YELP API KEY can be inserted here
  - {'Authorization': 'Bearer %s' % os.environ.get('YELP_API_KEY', 'YOUR_YELP_API_KEY')}
- The IPStack Key can be inserted here
  - geo_lookup = GeoLookup(os.environ.get('IPSTACK_API_KEY', 'YOUR_IP_STACK_KEY'))

#### App Features Include:

- User can create an account and have the ability to review restaurants and favorite restaurants they would like to visit. The user has the ability to also search restaurant based on keywords.

- Others users are able to like your reviews if they find them useful.

#### Original Site:

![Image of the Original Site](img/first-project.png 'Original Site')

#### Resources Used:

- Yelp API: [https://www.yelp.com/developers]

#### Technology Used:

- Python
- Flask
- JavaScript
- Bootstrap
- IPStack
