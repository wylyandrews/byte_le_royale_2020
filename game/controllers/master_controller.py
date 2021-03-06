from copy import deepcopy

from game.common.enums import *
from game.common.player import Player
from game.common.action import Action
from game.common.disasters import *
from game.common.city import City
import game.config as config

from game.controllers.controller import Controller
from game.controllers.city_generator_controller import CityGeneratorController
from game.controllers.decree_controller import DecreeController
from game.controllers.destruction_controller import DestructionController
from game.controllers.disaster_controller import DisasterController
from game.controllers.effort_controller import EffortController
from game.controllers.event_controller import EventController
from game.controllers.accumulative_controller import AccumulativeController
from game.controllers.fun_stat_controller import FunStatController


class MasterController(Controller):
    def __init__(self):
        super().__init__()

        self.turn = 0

        # Singletons first
        self.event_controller = EventController()
        self.fun_stat_controller = FunStatController()

        self.accumulative_controller = AccumulativeController()
        self.city_generator_controller = CityGeneratorController()
        self.decree_controller = DecreeController()
        self.destruction_controller = DestructionController()
        self.disaster_controller = DisasterController()
        self.effort_controller = EffortController()

        self.game_over = False

    # Receives all clients for the purpose of giving them the objects they will control
    def give_clients_objects(self, client):
        client.city = City()
        client.team_name = client.code.team_name()
        client.city.city_name = client.code.city_name()
        city_type = client.code.city_type()

        self.city_generator_controller.handle_actions(client, city_type)

    # Generator function. Given a key:value pair where the key is the identifier for the current world and the value is
    # the state of the world, returns the key that will give the appropriate world information
    def game_loop_logic(self, start=1):
        self.turn = start

        # Basic loop from 1 to max turns
        while True:
            # Wait until the next call to give the number
            yield self.turn
            # Increment the turn counter by 1
            self.turn += 1
            # If the next turn number is above the max, the iterator ends
            if self.turn > config.MAX_TURNS:
                break

    # Receives world data from the generated game log and is responsible for interpreting it
    def interpret_current_turn_data(self, client, world, turn):
        # Turn disaster occurrence into a real disaster
        for disaster in world['disasters']:
            d = disaster['disaster']
            l = disaster['level']
            dis = None
            if d is DisasterType.earthquake:
                dis = Earthquake(l)
            elif d is DisasterType.fire:
                dis = Fire(l)
            elif d is DisasterType.blizzard:
                dis = Blizzard(l)
            elif d is DisasterType.monster:
                dis = Monster(l)
            elif d is DisasterType.tornado:
                dis = Tornado(l)
            elif d is DisasterType.ufo:
                dis = Ufo(l)

            if dis is None:
                raise TypeError(f'Attempt to create disaster failed because given type: {disaster}, does not exist.')

            client.disasters.append(dis)

            self.fun_stat_controller.total_disasters += 1
            self.event_controller.add_event({
                "event_type": EventType.disaster_spawned,
                "turn": turn,
                "disaster": dis.to_json()
            })

        # Run decrees immediately after disasters are generated (before player has a chance to set a new one)
        self.decree_controller.execute_decree(client)

        # read the sensor results from the game map, converting strings to ints and/or floats
        world['sensors'] = {int(key): {int(key2): float(val2) for key2, val2 in val.items()} for key, val in world['sensors'].items()}

        # give client their corresponding sensor odds
        for sensor in client.city.sensors.values():
            sensor.sensor_results = world['sensors'][sensor.sensor_type][sensor.level]

        # Accumulations should occur before the player takes their turn
        self.accumulative_controller.update(client)

    # Receive a specific client and send them what they get per turn. Also obfuscates necessary objects.
    def client_turn_arguments(self, client, world, turn):
        actions = Action()
        client.action = actions

        obfuscated_city = deepcopy(client.city)
        obfuscated_city.obfuscate()
        for building in obfuscated_city.buildings.values():
            building.obfuscate()
        for sensor in obfuscated_city.sensors.values():
            sensor.obfuscate()

        obfuscated_disasters = deepcopy(client.disasters)
        for disaster in obfuscated_disasters:
            disaster.obfuscate()

        args = (self.turn, actions, obfuscated_city, obfuscated_disasters,)
        return args

    # Perform the main logic that happens per turn
    def turn_logic(self, client, world, turn):
        self.event_controller.update(turn)

        self.effort_controller.handle_actions(client)
        self.decree_controller.update_decree(client.action.get_decree())
        self.destruction_controller.handle_actions(client)
        self.disaster_controller.handle_actions(client)

        # Fun stat controller interjection
        self.fun_stat_controller.total_population_ever += client.city.population
        self.fun_stat_controller.total_structure_ever += client.city.structure

        if client.city.structure <= 0:
            self.print("Game is ending because city has been destroyed.")
            self.game_over = True

        if client.city.population <= 0:
            self.print("Game is ending because population has died.")
            self.game_over = True

    # Return serialized version of game
    def create_turn_log(self, client, world, turn):
        data = dict()

        # Retrieve all events on this turn
        data['events'] = [event for event in self.event_controller.get_events() if event.get('turn') == turn]

        data['rates'] = world['rates']

        data['player'] = client.to_json()

        return data

    # Gather necessary data together in results file
    def return_final_results(self, client, world, turn):
        # data is the json information what will be written to the results file
        data = {
            "Team": client.team_name,  # TODO: Replace with an engine-safe ID of each team
            "Score": turn,
            "Events": self.event_controller.get_events(),
            "Error": client.error,
            "Statistics": self.fun_stat_controller.export()
        }
        return data

    # Return if the game should be over
    def game_over_check(self):
        return self.game_over
