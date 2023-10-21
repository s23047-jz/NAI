import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

from classes.city import City


air_pollution_dict = {
	"pm10": {
		"very good": [0, 10, 20],
		"good": [20, 35, 50],
		"moderate": [50, 65, 80],
		"sufficient": [80, 95, 110],
		"bad": [110, 130, 150],
		"very bad": [150, 150, 600]
	},
	"pm25": {
		"very good": [0, 6.5, 13],
		"good": [13, 24, 35],
		"moderate": [35, 45, 55],
		"sufficient": [55, 65, 75],
		"bad": [75, 92.5, 110],
		"very bad": [110, 110, 600]
	},
	"o3": {
		"very good": [0, 35, 70],
		"good": [70, 95, 120],
		"moderate": [120, 135, 150],
		"sufficient": [150, 165, 180],
		"bad": [180, 210, 240],
		"very bad": [240, 240, 600],
		"index": 0
	},
	"no2": {
		"very good": [0, 20, 40],
		"good": [40, 70, 100],
		"moderate": [100, 125, 150],
		"sufficient": [150, 190, 230],
		"bad": [230, 315, 400],
		"very bad": [400, 400, 600],
		"index": 1
	},
	"so2": {
		"very good": [0, 25, 50],
		"good": [50, 75, 100],
		"moderate": [100, 150, 200],
		"sufficient": [200, 275, 350],
		"bad": [350, 425, 500],
		"very bad": [500, 500, 600]
	}
}

air_quality_dict = {
	"very good": 0,
	"good": 1,
	"moderate": 2,
	"sufficient": 3,
	"bad": 4,
	"very bad": 5
}


class CityAirQuality:
	def __init__(self, city: City):
		self.__city = city
		self.__antecedents = {}
		self.__consequent_dict = {}
		self.__mixture_of_air_particles = {
			"pm10": [0, 250],
			"pm25": [0, 200],
			"o3": [0, 340],
			"no2": [0, 500],
			"so2": [0, 600]
		}
		self.__air_quality_levels = [
			"very good", "good", "moderate", "sufficient", "bad", "very bad"
		]
		self.initialise()

	def _create_antecedent(self, param_name: str, universe_range: np.arange):
		self.__antecedents[param_name] = ctrl.Antecedent(universe_range, param_name)

	def _setup(self):

		for param_name, range_values in self.__mixture_of_air_particles.items():
			self._create_antecedent(param_name, np.arange(range_values[0], range_values[1] + 1, 1))

		for key in self.__mixture_of_air_particles.keys():
			for aql in self.__air_quality_levels:
				self.__antecedents[key][aql] = fuzz.trimf(
					self.__antecedents[key].universe, air_pollution_dict[key][aql]
				)

	def _create_consequent(self):
		for key in self.__mixture_of_air_particles.keys():
			cons = ctrl.Consequent(np.arange(0, 601, 1), key)
			for aql in self.__air_quality_levels:
				cons[aql] = fuzz.trimf(
					cons.universe, air_pollution_dict[key][aql]
				)
			self.__consequent_dict[key] = cons

	def _determine_air_quality(self, output_value, variable_name):
		air_quality_levels = air_pollution_dict.get(variable_name, {})

		for level, (low, mid, high) in air_quality_levels.items():
			if low <= output_value <= high:
				return level

	def _evaluate_air_quality(self):
		self._create_consequent()
		results_dict = {}

		for key in self.__mixture_of_air_particles.keys():
			rules = []
			for aql in self.__air_quality_levels:
				rule = ctrl.Rule(self.__antecedents[key][aql], self.__consequent_dict[key][aql])
				rules.append(rule)
			result_ctrl = ctrl.ControlSystem(rules)
			result = ctrl.ControlSystemSimulation(result_ctrl)
			result.input[key] = self.__city.to_dict()[key]
			results_dict[key] = result

		city_air_quality_arr = []
		for key in self.__mixture_of_air_particles.keys():
			result = results_dict[key]
			result.compute()
			city_air_quality_arr.append(
				self._determine_air_quality(result.output[key], key)
			)
			self.__consequent_dict[key].view(sim=result)

		# TODO finish get air quality
		city_air_quality_dict = {
			air_quality_dict[key]
			for key in city_air_quality_arr
		}




	def show(self):
		self._setup()
		for param_name, antecedent in self.__antecedents.items():
			antecedent.view()

		plt.show()

	def initialise(self):
		self._setup()
		# self.show()
		self._evaluate_air_quality()
