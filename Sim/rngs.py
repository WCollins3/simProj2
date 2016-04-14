

# NOTE: This version does not support PlantSeeds(0)!

import time


def random():
    t = int(random.MULTIPLIER * (random.seeds[random.stream] % random.Q) -
            random.R * (random.seeds[random.stream] // random.Q))
    if t > 0:
        random.seeds[random.stream] = t
    else:
        random.seeds[random.stream] = t + random.MODULUS

    return random.seeds[random.stream] / random.MODULUS


# Constants that define the behavior.  DO NOT CHANGE.
random.MODULUS = 2147483647
random.MULTIPLIER = 48271
random.JUMP_MULTIPLIER = 22925
random.NUM_STREAMS = 256
random.Q = random.MODULUS // random.MULTIPLIER
random.R = random.MODULUS % random.MULTIPLIER

# Run with 1 seed unless streams are enabled
random.seeds = [123456789]
random.stream = 0


def put_seed(seed):
    if seed <= 0:
        random.seeds[random.stream] = int(time.time()) % random.MODULUS
    else:
        random.seeds[random.stream] = seed % random.MODULUS


def get_seed():
    return random.seeds[random.stream]


def plant_seeds(seed):

    quotient = int(random.MODULUS / random.JUMP_MULTIPLIER)
    remainder = int(random.MODULUS % random.JUMP_MULTIPLIER)
    random.seeds = []

    curr_seed = seed

    for count in range(random.NUM_STREAMS):
        random.seeds.append(curr_seed)

        t = int(random.JUMP_MULTIPLIER * (curr_seed % quotient) - remainder * int((curr_seed / quotient)))
        if t > 0:
            curr_seed = t
        else:
            curr_seed = t + random.MODULUS


def select_stream(stream_num):
    # Use mod to ensure we don't set a stream out of range
    random.stream = stream_num % len(random.seeds)


