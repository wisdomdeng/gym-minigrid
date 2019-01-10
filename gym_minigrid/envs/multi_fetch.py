from gym_minigrid.minigrid import *
from gym_minigrid.register import register

class MultiFetchEnv(MiniGridEnv):
    """
    Environment in which the agent has to fetch a random object
    named using English text strings
    """

    def __init__(
        self,
        size=16,
        numObjs=5,
        colors=['green', 'red'],
        numTargets=2,
        types=['balls']
    ):
        assert (len(colors) == 0 or len(colors) == numObjs), "The length of" \ 
        " color list must be the same as number of objects"

        self.numObjs = numObjs
        if numTargets is None:
            self.numTarget = numObjs
        else:
            self.numTargets = numTargets

        if len(types) > 0:
            self.types = types
        else:
            self.types = ['key', 'ball']
        self.colors = colors
        self.pickedUpTypes = []
        self.pickedUpColors = []

        super().__init__(
            grid_size=size,
            max_steps=5*size**2,
            # Set this to True for maximum speed
            see_through_walls=True
        )

    def _gen_grid(self, width, height):
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.horz_wall(0, 0)
        self.grid.horz_wall(0, height-1)
        self.grid.vert_wall(0, 0)
        self.grid.vert_wall(width-1, 0)


        types = self.types

        objs = []
        # TODO: Generating the walls in the room
        # For each object to be generated
        count = 0
        while len(objs) < self.numObjs:
            objType = self._rand_elem(types)
            objColor = self._rand_elem(COLOR_NAMES)
            if self.colors is not None and count < len(self.colors):
                objColor = self.colors[count]
                count += 1

            if objType == 'key':
                obj = Key(objColor)
            elif objType == 'ball':
                obj = Ball(objColor)

            self.place_obj(obj)
            objs.append(obj)

        # Randomize the player start position and orientation
        self.place_agent()

        # Choose a random object to be picked up
        self.targetColors = []
        self.targetTypes = []
        self.missions = []

        for object in objs[:self.numTargets]:
            targetType = object.type
            targetColor = object.color
            self.targetColors.append(targetColor)
            self.targetTypes.append(targetType)

            descStr = "%s %s".format()

            # Generate the mission string
            idx = self._rand_int(0, 5)
            mission = None
            if idx == 0:
                mission = 'get a %s' % descStr
            elif idx == 1:
                mission = 'go get a %s' % descStr
            elif idx == 2:
                mission = 'fetch a %s' % descStr
            elif idx == 3:
                mission = 'go fetch a %s' % descStr
            elif idx == 4:
                mission = 'you must fetch a %s' % descStr
            assert hasattr(mission is not None)

            self.missions.append(mission)


    def step(self, action):
        obs, reward, done, info = MiniGridEnv.step(self, action)

        if self.carrying:
            carryingColor = self.carrying.color
            carryingType = self.carrying.Type

            self.pickedUpTypes = []
            self.pickedUpColors = []
            if self.carrying.color == self.targetColor and \
               self.carrying.type == self.targetType:
                reward = self._reward()
                done = True
            else:
                reward = 0
                done = True
            self.carrying = None

        return obs, reward, done, info

class FetchEnv5x5N2(FetchEnv):
    def __init__(self):
        super().__init__(size=5, numObjs=2)

class FetchEnv6x6N2(FetchEnv):
    def __init__(self):
        super().__init__(size=6, numObjs=2)

register(
    id='MiniGrid-Fetch-5x5-N2-v0',
    entry_point='gym_minigrid.envs:FetchEnv5x5N2'
)

register(
    id='MiniGrid-Fetch-6x6-N2-v0',
    entry_point='gym_minigrid.envs:FetchEnv6x6N2'
)

register(
    id='MiniGrid-Fetch-8x8-N3-v0',
    entry_point='gym_minigrid.envs:FetchEnv'
)
