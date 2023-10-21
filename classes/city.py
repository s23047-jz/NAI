import requests


GIOS_ENDPOINTS = {
	"all": "https://api.gios.gov.pl/pjp-api/rest/station/findAll",
	"index": "https://api.gios.gov.pl/pjp-api/rest/station/sensors",
	"air_particles": 'https://api.gios.gov.pl/pjp-api/rest/data/getData'
}


def create_dict_for_city(
	name: str,
	pm10: float,
	pm25: float,
	o3: float,
	no2: float,
	so2: float
):
	return {
		"name": name,
		"pm10": pm10,
		"pm25": pm25,
		"o3": o3,
		"no2": no2,
		"so2": so2
	}


class City:
	def __init__(self, get_data_from_api: bool = False, city_index: int = 1):
		self.__get_data_from_api = get_data_from_api
		self.__city_index = city_index
		self.name = 'Test'
		self.pm10 = 0
		self.pm25 = 0
		self.o3 = 0
		self.no2 = 0
		self.so2 = 0

	def _set_city_value(
		self,
		key: str,
		value: float
	):
		setattr(self, key, value)

	def _get_all_cities(self):
		try:
			r = requests.get(GIOS_ENDPOINTS['all'])
			data = r.json()

			city = data[self.__city_index]
			self.__name = city['city']['name']

			self._get_city_data(city['id'])

		except Exception as e:
			print(f"Something went wrong: {str(e)}")

	def _get_city_data(self, id: int):
		try:
			r = requests.get(
				f"{GIOS_ENDPOINTS['index']}/{id}"
			)
			data = r.json()

			for obj in data:
				self._get_air_particles(obj['id'])
		except Exception as e:
			print(f"Something went wrong: {str(e)}")

	def _get_air_particles(self, id: int):
		try:
			r = requests.get(
				f"{GIOS_ENDPOINTS['air_particles']}/{id}"
			)
			data = r.json()

			# data['values'][0]['value'] => latest value
			self._set_city_value(
				key=data['key'].lower(),
				value=data['values'][0]['value']
			)
		except Exception as e:
			print(f"Something went wrong: {str(e)}")

	def _get_data_from_api(self):
		self._get_all_cities()

	def _create_custom_city(self, dict_of_values: dict):
		city_keys = ["name", "pm10", "pm25", "o3", "no2", "so2"]
		for city_key in city_keys:
			if city_key in dict_of_values.keys():
				if city_key == 'name':
					self.__name = dict_of_values['name']
				else:
					self._set_city_value(
						key=city_key, value=float(dict_of_values[city_key])
					)

	def initialise(self, dict_of_values: dict = None):
		if self.__get_data_from_api:
			self._get_data_from_api()
		elif not self.__get_data_from_api and dict_of_values is not None:
			self._create_custom_city(dict_of_values)
		else:
			print("Nothing happened")

	def to_dict(self):
		return {
			"name": self.name,
			"pm10": self.pm10,
			"pm25": self.pm25,
			"o3": self.o3,
			"no2": self.no2,
			"so2": self.so2
		}

	def show(self):
		print(self.to_dict())
