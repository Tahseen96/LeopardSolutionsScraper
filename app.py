import eel
from scraper import main,LeopardSolutionsScraper
from cities import international,south,west,remote,midwest,northeast
  
creds = None
# Exposing the random_python function to javascript
@eel.expose
def run_main(locations, sublocations, cities_locations, practice_area, keyword_search_string, keyword_type, keyword_find_with, firms, languages, honors, types, specialties, admits, status1, status2, min_salary, max_salary, exports):
    for index,city in enumerate(cities_locations):
        cities_locations[index] = city.replace("-"," ")
    non_selected_cities = {}
    for location in sublocations:
        try:
            if international[location]:
                for city in cities_locations:
                    if city in international[location]:
                        international[location].remove(city)
                        non_selected_cities[location] = international[location]
        except: ()
        try:
            if south[location]:
                for city in cities_locations:
                    if city in south[location]:
                        south[location].remove(city)
                        non_selected_cities[location] = south[location]
        except: ()
        try:
            if west[location]:
                for city in cities_locations:
                    if city in west[location]:
                        west[location].remove(city)
                        non_selected_cities[location] = west[location]
        except:()
        try:
            if remote[location]:
                for city in cities_locations:
                    if city in remote[location]:
                        remote[location].remove(city)
                        non_selected_cities[location] = remote[location]
        except: ()
        try:
            if midwest[location]:
                for city in cities_locations:
                    if city in midwest[location]:
                        midwest[location].remove(city)
                        non_selected_cities[location] = midwest[location]
        except: ()
        try:
            if northeast[location]:
                for city in cities_locations:
                    if city in northeast[location]:
                        northeast[location].remove(city)
                        non_selected_cities[location] = northeast[location]
        except: ()
    # print(locations, sublocations, non_selected_cities, practice_area, keyword_search_string, keyword_type, keyword_find_with, firms, languages, honors, types, specialties, admits, status1, status2, min_salary, max_salary, exports)
    main(creds, locations, sublocations, non_selected_cities, practice_area, keyword_search_string, keyword_type, keyword_find_with, firms, languages, honors, types, specialties, admits, status1, status2, min_salary, max_salary, exports)
    return
  
# Start the index.html file
if __name__ == '__main__':
    creds = LeopardSolutionsScraper.check_token_expiration()
    eel.init("web")  
    eel.start("index.html", size=(1590, 720), port=0, mode='chrome')