class Shipmanager:

    def __init__(self, navigator, map_analyzer):
        self.navigator = navigator
        self.map_analyzer = map_analyzer
        self.targets = self._build_targets()
        self.ships = {}  # ship_id: Comman_que

    def next_step(self, ship):
        ship_id = ship.id
        if ship_id not in self.ships.keys():  # in case the ship is new
            self.ships[ship_id] = []
        if self.ships[ship_id]:  # in case the ship still has an ongoing task
            return self.execute_task(self.ships[ship_id][0])
        else:  # ship is not new and has no ongoing task
            self.ships[ship_id].append(self.create_task(ship))
            return self.ships[ship_id][0]

    def execute_task(self, task, ship):
        if task.name == "Navigation":
            self.navigator.navigate_to(ship.position, task.location)
        if task.name:
            pass

    def create_task(self, ship):
        pass
        # find target
        # navigate to it
        # farm kernel


    def request_target(self, ship_id, target_id):
        if self.targets[target_id]["owned_by"]:
            return False
        else:
            self.targets[target_id]['owned_by'] = ship_id
            return True

    def change_ship_state(self, ship_id):
        return False




    def _build_targets(self):
        targets = {}
        for spot in self.map_analyzer.honey_spots:
            targets[spot.node] = {"element": spot, "owned_by": None}
        return targets




class Task:

    def __init__(self):
        pass
    def next(self):
        return 1

class NavigationTask:

    pass

class FarmingTask:
    pass

class KillTask:
    pass

class InfraStrukturTask:
    pass