# Green Eats 🍽🌿
### project description 

* Building a web-app that that calculates the carbon footprint of the ingredients in a given
recipe and to help users make more sustainable meal choices (ideally recommends more sustainable alternatives.)
* It calculates the carbon footprint of the ingredients in a given recipe and recommends more sustainable alternatives
* The goal of the project is to have an MVP (minimum viable product).
* This means we aim at having something that works, not necessarily the best (in terms of design and range of possible visualizations/functions).

### A web application containing:
*  A tool to parse ingredients from a recipe and calculate the carbon footprint.
*  A system to make personalised sustainable recommendations.
* A dashboard to visualise the carboon footprint of the recipes/ingredients in the database.

### Background & Motiavation 
* The current worldwide food production accounts for more than a quarter of total greenhouse gas emissions, which in turn is the leading cause of climate change (Ripple et al. 2017).
* Consumers’ food decisions can play a fundamental role in reducing the carbon footprint (Hirsch and Terlau 2015; Verbeke and Vackier 2004) by for example aligning with a more sustainable food diet, where environmentally harmful products (i.e., high in CO2 emissions) have a lower preponderance.
* CO2 emissions associated with food consumption is a relatively new and abstract concept, that consumers cannot (yet) properly digest.
* Therefore, supportive and guidance instruments are needed to help consumers make more sustainable decisions.

### Functionality 
* Input a recipe by either scraping it from food.com or by manually inputting the ingredients & quantities.
* Estimate the CO2 score per ingredients and per recipe.
* Recommend recipes that could be similar in taste, but with lower carbon footprint.
* Dashboard with meaningful insights about the carbon footprint of the recipes in the database

### App architecture
* Database
  * Store the raw recipes scraped by the user
  * Store the parsed recipes
  * Store the CO2 scores corresponding to each recipe/ingredient
  * Store recipe recommendations
  * Store data to be shown in the dasboard
* Backend
  * Connect to the database with the reference data and copy it to your database.
  * Scrape food.com page based on recipe URL.
  * Process & standardise recipe ingredients.
  * Calculate CO2 scores
  * Recommend similar but more sustainable recipes.
  * Write results in your Cloud SQL database
* Frontend
  * Intuitive user interface with interactive tools (input: recipe URL from food.com, output : CO2 score and recommended recipes)
  * Dashboard with relevant insights.

### Technology stacks 
1. Python (dash, flask, scikit-learn)
2. SQL (postgreSQL)
3. Google Cloud Platform (https://cloud.google.com/)
4. Datastudio (https://datastudio.google.com/)

### Focus of deliverables 
* We aim at delivering a prototype which can be directly used by researchers.
* Therefore, the focus is the functionality of the web application.
* This means we aim at having something which works well and which can be easily
further developed.
* We did not target to develop the best and complex solution with the SOTA AI
recommendation algorithm 

### Development process
1. Set up infrastructure on GCP
* Setup the backend server
* Setup the frontend server
* Setup the database (Cloud SQL server)
* Deploy the demo app 

2. Create the app
* Create the back-end APIs (R: plumber; Python: flask /django)
* Create the front-end (R: shiny; Python: flask / django)
* Create the dashboard (Google Datastudio)

3. Deploy and test
* Deploy the backend (first configure to communicate with the database)
* Publish the dashboard 
* Deploy the front-end (first configure to communicate with the the backend and the
dashboard)
