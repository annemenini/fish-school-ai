import argparse
import os

import numpy as np
import open3d


class Position:
    def __init__(self, x=None, y=None, z=None):
        self.x = x if x is not None else np.random.uniform()
        self.y = y if y is not None else np.random.uniform()
        self.z = z if z is not None else np.random.uniform()

    def as_array(self):
        return np.array([self.x, self.y, self.z])


class Direction:
    def __init__(self, x=None, y=None, z=None):
        xy_speed = flags.random_step_rl
        z_speed = flags.random_step_dv
        self.x = x if x is not None else np.random.uniform(-xy_speed, xy_speed)
        self.y = y if y is not None else np.random.uniform(-xy_speed, xy_speed)
        self.z = z if z is not None else np.random.uniform(-z_speed, z_speed)


class Color:
    def __init__(self, r=None, g=None, b=None):
        self.r = r if r is not None else np.random.randint(256)
        self.g = g if g is not None else np.random.randint(256)
        self.b = b if b is not None else np.random.randint(256)


class Fish:
    def __init__(self, position=None, direction=None, color=None):
        self.position = position if position is not None else Position()
        self.direction = direction if direction is not None else Direction()
        self.color = color if color is not None else Color()

    def position_array(self):
        return self.position.as_array()


class School:
    def __init__(self, num_fish, dumping_location):
        self.fishes = [Fish() for _ in range(num_fish)]
        self.discrete_space = self._update_discrete_space()
        self.dumping_location = dumping_location

    def _update_discrete_space(self):
        discrete_dim_x = np.floor(flags.space_dim_x / flags.attraction_radius)
        discrete_dim_y = np.floor(flags.space_dim_y / flags.attraction_radius)
        discrete_dim_z = np.floor(flags.space_dim_z / flags.attraction_radius)
        discrete_space = np.empty((discrete_dim_x, discrete_dim_y, discrete_dim_z), dtype=object)

        discrete_step_x = flags.space_dim_x / discrete_dim_x
        discrete_step_y = flags.space_dim_y / discrete_dim_y
        discrete_step_z = flags.space_dim_z / discrete_dim_z

        for fish in self.fishes:
            discrete_position_x = np.floor(fish.position.x / discrete_step_x)
            discrete_position_y = np.floor(fish.position.y / discrete_step_y)
            discrete_position_z = np.floor(fish.position.z / discrete_step_z)
            discrete_space[discrete_position_x, discrete_position_y, discrete_position_z].append(fish)

        return discrete_space

    def animate_step(self):
        return

    def dump_configuration(self):
        return

    def display(self):
        point_cloud = np.stack([fish.position_array() for fish in self.fishes], axis=0)
        open3d.visualization.draw_geometries([point_cloud])

    def dump_and_display(self):
        self.dump_configuration()
        if flags.display:
            self.display()


def main():
    school = School(flags.num_fish, flags.dumpig_location)
    school.dump_and_display()
    for _ in range(flags.num_step):
        school.animate_step()
        school.dump_and_display()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--num_fish', type=int, default=8, help='Number of fishes composing the school.')
    parser.add_argument('--num_step', type=int, default=16, help='Number of animation steps to simulate.')
    parser.add_argument('--space_dim_x', type=float, default=1, help='Size of the space along x.')
    parser.add_argument('--space_dim_y', type=float, default=1, help='Size of the space along y.')
    parser.add_argument('--space_dim_z', type=float, default=1, help='Size of the space along z.')
    parser.add_argument('--dumping_location', type=str, default=os.getcwd(),
                        help='Location where to dump the school configuration for each step.')
    parser.add_argument('--display', type=bool, default=False,
                        help='Display the animation at each step.')
    parser.add_argument('--attraction_strength', type=float, default=1, help='Strength of the attraction rule.')
    parser.add_argument('--attraction_radius', type=float, default=0.2,
                        help='Range of application of the attraction rule.')
    parser.add_argument('--repulsion_strength', type=float, default=2, help='Strength of the repulsion rule.')
    parser.add_argument('--repulsion_radius', type=float, default=0.02,
                        help='Range of application of the repulsion rule.')
    parser.add_argument('--inertia_strength_ap', type=float, default=1,
                        help='Strength of the inertia rule along the antero-posterior direction.')
    parser.add_argument('--inertia_strength_rl', type=float, default=0.5,
                        help='Strength of the inertia rule along the right-left direction.')
    parser.add_argument('--inertia_strength_dv', type=float, default=2,
                        help='Strength of the inertia rule along the dorso-ventral direction.')
    parser.add_argument('--random_step_ap', type=float, default=0.01,
                        help='Additional random step in the antero-posterior direction.')
    parser.add_argument('--random_step_rl', type=float, default=0.02,
                        help='Additional random step in the right-left direction.')
    parser.add_argument('--random_step_dv', type=float, default=0.005,
                        help='Additional random step in the dorso-ventral direction.')

    flags, _ = parser.parse_known_args()

    main()
