# Understanding Access to Restaurants Through Personas: A Latent Class Approach Integrating Preferences and Travel Behavior

**Abstract**: Access to food plays a key role in one’s health and well-being. Past studies on food access have primarily focused on grocery stores. Eating out, however, consumes on average 5.1% of Americans’ disposable income. In this paper, we study how individuals’ restaurant preferences and travel behavior may be bundled together to form different personas and how each persona may be related to the built environment and socioeconomic demographics. Latent class analysis is performed using data from the Puget Sound Regional Council 2017-2019 Household Travel Survey. The study finds four personas: Convenient Eaters, Lunch Breakers, Restaurant Explorers and Fast Food Enthusiasts. Restaurant-related travel behavior is significantly impacted by the number of children in a household, vehicle access and age, though it is not constrained for those who live in a food desert. Differences in travel time, frequency of restaurant trips and meal time are observed between personas. The findings of this study suggest that interventions toward healthy eating could be tailored to the specific needs of each persona. 

**[manuscript link pending!]**

# Data
This data is from the [PSRC household travel survey](https://www.psrc.org/our-work/household-travel-survey-program) (2017, 2019) with additional information on people's travel patterns through smartphone traces which cannot be made public. This data is fused with [Yelp data](https://docs.developer.yelp.com/docs/fusion-intro) and [American Census Survey data](https://data.census.gov/).

# Workflow & repo structure
## Repo structure
#### Folders:
- `data_inputs`: PSRC HTS (trip, person, household data, origin-destination + home lat/lon-- **cannot be made public for privacy purposes**); ACS built environment data
- `data_outputs`: outputs from data cleaning/wrangling from trip-level data
- `mplus_analysis`: contains all files for analysis in Mplus (data, input/outputs for 2-step process)
- `figures`: contains figures used in manuscript


#### Scripts:
- `person_data.ipynb`: processes HTS data to select all trip data for persons who make restaurant trips, all cleaning. Aggregates restaurant preferences to person level and adds in built environment variables.
  - Cleaning: restaurant trips with a calculated travel time > 120 mins, 2021 trips, weekend trips were dropped. 
  - Dataset info: 4,048 people who made 69,340 non-restaurant trips and 14,447 restaurant trips.
  - Input: PSRC HTS (person, trip), USDA food access research atlas data (uses 2010 census data), 2019 census data (median income, population), Yelp data
  - Output: 
    - `data_outputs/trips_od_rest.csv`: trips of individuals who made restaurant trips, with O/D information (**removed from repo for privacy purposes**)
    - `data_outputs/final_person_data.csv`: cleaned, processed data aggregating trips to the person-level
- `yelp_scraper.py`: uses Yelp Rest API to add POI data into restaurant trip dataset.
    - Input: `data_outputs/trips_od_rest.csv`
    - Output: `data_outputs/trips_od_yelp_1[2,3,4,5].csv`
- `data_for_lca.ipynb`: processes data to be compatible with Mplus for LCA. selects variables used in analysis.
  - Input: `data_outputs/final_person_data.csv`
  - Output: `data_outputs/lca_data.csv`


## Workflow
1. Process HTS data, create HTS + ACS dataset at trip level using `person_data.ipynb`
2. Obtain restaurant information via Yelp API for each restaurant trip using `yelp_scraper_threading.py`
3. Process restaurant data from previous step and aggregate variables of interest to person-level using `person_data.ipynb`
4. Reformat data to be compatible with Mplus using `data_for_lca.ipynb`
5. Perform two-step analysis in Mplus by running `.inp` files in `mplus_final`, output `4_class_probabilities.dat` for further analysis
6. Create visualizations in `membership_radar_plots.ipynb` (radar plots) and `results_visualizations.ipynb` (class enumeration, indicator and covariate tables)



