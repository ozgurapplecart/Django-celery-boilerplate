import googlemaps
import populartimes
import time


class GoogleDataGetter:
    def __init__(self):
        self.API_KEY = 'AIzaSyBgxu9OTX8OHr3W6njmUaZZO8-6iDl4Hss'
        self.gmaps = googlemaps.Client(key=self.API_KEY)

    def run_for_a_location(self, lat, long, keyword, radius=50000):
        all_results = []
        page_token = None
        while True:
            results = self.gmaps.places_nearby(location=(lat, long),
                                               radius=radius,
                                               keyword=keyword,
                                               page_token=page_token)
            time.sleep(3)
            if 'next_page_token' in results:
                page_token = results['next_page_token']
                print(page_token)
                all_results = all_results + results['results']
            else:
                all_results = all_results + results['results']
                break

        place_ids_and_places = [(place['place_id'], place) for place in all_results]

        places_by_gid = {}
        for k in range(len(place_ids_and_places)):
            places_by_gid[str(place_ids_and_places[k][0])] = {**place_ids_and_places[k][1],
                                                              **populartimes.get_id(self.API_KEY,
                                                                                    place_ids_and_places[k][0])}
            time.sleep(1)

        return places_by_gid
