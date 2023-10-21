"""
Authors:
    Jakub Żurawski: https://github.com/s23047-jz/connect_four
    Mateusz Olstowski: https://github.com/Matieus/connect_four
"""

from classes.air_pollution import AirPollution
from classes.city import City, create_dict_for_city


def main():
    # air_pollution = AirPollution()
    # air_pollution.show()
    # city = City(get_data_from_api=True, city_index=0)
    city = City()
    city.initialise(create_dict_for_city(
        name="Test",
        pm10=15.23,
        pm25=12.25,
        o3=50.03,
        no2=2.0,
        so2=9.56
    ))
    city.show()


if __name__ == "__main__":
    main()
