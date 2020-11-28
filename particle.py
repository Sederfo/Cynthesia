import pygame


class Particle:
    def __init__(self, position, radius, velocity, lifespan, color):
        self.position = position
        self.radius = radius
        self.velocity = velocity
        self.lifespan = lifespan
        self.color = color
