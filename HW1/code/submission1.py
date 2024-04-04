from typing import List, Tuple, Dict

from mapUtil import (
    CityMap,
    computeDistance,
    createStanfordMap,
    locationFromTag,
    makeTag,
)
from util import Heuristic, SearchProblem, State, UniformCostSearch

# BEGIN_YOUR_CODE (You may add some codes here to assist your coding below if you want, but don't worry if you deviate from this.)

# END_YOUR_CODE

# *IMPORTANT* :: A key part of this assignment is figuring out how to model states
# effectively. We've defined a class `State` to help you think through this, with a
# field called `memory`.
#
# As you implement the different types of search problems below, think about what
# `memory` should contain to enable efficient search!
#   > Check out the docstring for `State` in `util.py` for more details and code.

########################################################################################
# Problem 1a: Modeling the Shortest Path Problem.


class ShortestPathProblem(SearchProblem):
    """
    Defines a search problem that corresponds to finding the shortest path
    from `startLocation` to any location with the specified `endTag`.
    """

    def __init__(self, startLocation: str, endTag: str, cityMap: CityMap):
        self.startLocation = startLocation
        self.endTag = endTag
        self.cityMap = cityMap

    def startState(self) -> State:
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return State(location = self.startLocation,  memory = None)
        # raise Exception("Not implemented yet")
        # END_YOUR_CODE

    def isEnd(self, state: State) -> bool:
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        if self.endTag in self.cityMap.tags[state.location]:
            return 1
        else:
            return 0
        # raise Exception("Not implemented yet")
        # END_YOUR_CODE

    def successorsAndCosts(self, state: State) -> List[Tuple[str, State, float]]:
        # BEGIN_YOUR_CODE (our solution is 7 lines of code, but don't worry if you deviate from this)
        successors = []
        for new_state_label, distance in self.cityMap.distances[state.location].items():
            new_state = State(location=new_state_label, memory=None)
            successors.append((new_state_label, new_state, distance))
        return successors
        # raise Exception("Not implemented yet")
        # END_YOUR_CODE


########################################################################################
# Problem 1b: Custom -- Plan a Route through Stanford


def getStanfordShortestPathProblem() -> ShortestPathProblem:
    """
    Create your own search problem using the map of Stanford, specifying your own
    `startLocation`/`endTag`. If you prefer, you may create a new map using via
    `createCustomMap()`.

    Run `python mapUtil.py > readableStanfordMap.txt` to dump a file with a list of
    locations and associated tags; you might find it useful to search for the following
    tag keys (amongst others):
        - `landmark=` - Hand-defined landmarks (from `data/stanford-landmarks.json`)
        - `amenity=`  - Various amenity types (e.g., "park", "food")
        - `parking=`  - Assorted parking options (e.g., "underground")
    """
    cityMap = createStanfordMap()

    # Or, if you would rather use a custom map, you can uncomment the following!
    # cityMap = createCustomMap("data/custom.pbf", "data/custom-landmarks".json")

    # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
    # raise Exception("Not implemented yet")
    startLocation = locationFromTag(makeTag("landmark", "gates"), cityMap)
    endTag = makeTag("landmark", "green_library")
    # END_YOUR_CODE
    return ShortestPathProblem(startLocation, endTag, cityMap)


########################################################################################
# Problem 2a: Modeling the Waypoints Shortest Path Problem.


class WaypointsShortestPathProblem(SearchProblem):
    """
    Defines a search problem that corresponds to finding the shortest path from
    `startLocation` to any location with the specified `endTag` such that the path also
    traverses locations that cover the set of tags in `waypointTags`.

    Think carefully about what `memory` representation your States should have!
    """
    def __init__(
        self, startLocation: str, waypointTags: List[str], endTag: str, cityMap: CityMap
    ):
        self.startLocation = startLocation
        self.endTag = endTag
        self.cityMap = cityMap

        # We want waypointTags to be consistent/canonical (sorted) and hashable (tuple)
        self.waypointTags = tuple(sorted(waypointTags))

    def startState(self) -> State:
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        # raise Exception("Not implemented yet")
        visited_if = tuple(([0 for _ in range(len(self.waypointTags))]))
        return State(location=self.startLocation, memory=visited_if)
        # END_YOUR_CODE

    def isEnd(self, state: State) -> bool:
        # BEGIN_YOUR_CODE (our solution is 5 lines of code, but don't worry if you deviate from this)
        # raise Exception("Not implemented yet")
        if self.endTag in self.cityMap.tags[state.location]:
            if all(element == 1 for element in state.memory):
                return 1
        return 0
        # END_YOUR_CODE

    def successorsAndCosts(self, state: State) -> List[Tuple[str, State, float]]:
        # BEGIN_YOUR_CODE (our solution is 17 lines of code, but don't worry if you deviate from this)
        successors = []
        for new_state_label, distance in self.cityMap.distances[state.location].items():
            new_memory = tuple(int(state.memory[i] or self.waypointTags[i] in self.cityMap.tags[new_state_label]) for i in range(len(self.waypointTags)))
            new_state = State(location=new_state_label, memory=new_memory)
            successors.append((new_state_label, new_state, distance))
        return successors
        # raise Exception("Not implemented yet")
        # END_YOUR_CODE


########################################################################################
# Problem 2b: Custom -- Plan a Route with Unordered Waypoints through Stanford


def getStanfordWaypointsShortestPathProblem() -> WaypointsShortestPathProblem:
    """
    Create your own search problem using the map of Stanford, specifying your own
    `startLocation`/`waypointTags`/`endTag`.

    Similar to Problem 1b, use `readableStanfordMap.txt` to identify potential
    locations and tags.
    """
    cityMap = createStanfordMap()
    # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
    # raise Exception("Not implemented yet")
    startLocation = "8763079035"
    endTag = makeTag("landmark", "green_library")
    waypointTags = [makeTag("amenity", "food"), makeTag("landmark", "tressider"), makeTag("landmark", "stanford_stadium")]
    # END_YOUR_CODE
    return WaypointsShortestPathProblem(startLocation, waypointTags, endTag, cityMap)


########################################################################################
# Problem 3a: A* to UCS reduction

# Turn an existing SearchProblem (`problem`) you are trying to solve with a
# Heuristic (`heuristic`) into a new SearchProblem (`newSearchProblem`), such
# that running uniform cost search on `newSearchProblem` is equivalent to
# running A* on `problem` subject to `heuristic`.
#
# This process of translating a model of a problem + extra constraints into a
# new instance of the same problem is called a reduction; it's a powerful tool
# for writing down "new" models in a language we're already familiar with.


def aStarReduction(problem: SearchProblem, heuristic: Heuristic) -> SearchProblem:
    class NewSearchProblem(SearchProblem):
        def startState(self) -> State:
            # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
            # raise Exception("Not implemented yet")
            return problem.startState()
            # END_YOUR_CODE

        def isEnd(self, state: State) -> bool:
            # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
            # raise Exception("Not implemented yet")
            return problem.isEnd(state)
            # END_YOUR_CODE

        def successorsAndCosts(self, state: State) -> List[Tuple[str, State, float]]:
            # BEGIN_YOUR_CODE (our solution is 8 lines of code, but don't worry if you deviate from this)
            # raise Exception("Not implemented yet")
            successors = []
            for new_state_label, distance in problem.cityMap.distances[state.location].items():
                new_state = State(location=new_state_label, memory=state.memory)
                distance = distance + heuristic.evaluate(new_state) - heuristic.evaluate(state)
                successors.append((new_state_label, new_state, distance))
            return successors
            # END_YOUR_CODE

    return NewSearchProblem()


########################################################################################
# Problem 3b: "straight-line" heuristic for A*


class StraightLineHeuristic(Heuristic):
    """
    Estimate the cost between locations as the straight-line distance.
        > Hint: you might consider using `computeDistance` defined in `mapUtil.py`
    """
    def __init__(self, endTag: str, cityMap: CityMap):
        self.endTag = endTag
        self.cityMap = cityMap

        # Precompute
        # BEGIN_YOUR_CODE (our solution is 5 lines of code, but don't worry if you deviate from this)
        # raise Exception("Not implemented yet")
        self.end_geolocation = []
        for location, tags in self.cityMap.tags.items():
            if endTag in tags:
                self.end_geolocation.append(self.cityMap.geoLocations[location])
        # END_YOUR_CODE

    def evaluate(self, state: State) -> float:
        # BEGIN_YOUR_CODE (our solution is 6 lines of code, but don't worry if you deviate from this)
        # raise Exception("Not implemented yet")
        state_geolocation = self.cityMap.geoLocations[state.location]
        distances = []
        for end_geolocation in self.end_geolocation:
            distances.append(computeDistance(state_geolocation, end_geolocation))
        straight_line_distance = min(distances)
        return straight_line_distance
        # END_YOUR_CODE


########################################################################################
# Problem 3c: "no waypoints" heuristic for A*


class NoWaypointsHeuristic(Heuristic):
    """
    Returns the minimum distance from `startLocation` to any location with `endTag`,
    ignoring all waypoints.
    """
    def __init__(self, endTag: str, cityMap: CityMap):
        # Precompute
        # BEGIN_YOUR_CODE (our solution is 25 lines of code, but don't worry if you deviate from this)
        # raise Exception("Not implemented yet")
        self.endTag = endTag
        self.cityMap = cityMap
        self.end_location = []
        for location, tags in self.cityMap.tags.items():
            if endTag in tags:
                self.end_location.append(location)
 
        self.loc_costs = {}
        for loc in self.end_location:
            ucs = UniformCostSearch()
            ucs.solve(ShortestPathProblem(loc, "label=0", cityMap))
            for state_loc, cost in ucs.pastCosts.items():
                self.loc_costs[(state_loc, loc)] = cost
        
        # END_YOUR_CODE

    def evaluate(self, state: State) -> float:
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        # raise Exception("Not implemented yet")
        state_cost = [self.loc_costs[(state.location, end_loc)] for end_loc in self.end_location if (state.location, end_loc) in self.loc_costs and self.loc_costs[(state.location, end_loc)] is not None]
        return min(state_cost) if state_cost else 0
        # END_YOUR_CODE
