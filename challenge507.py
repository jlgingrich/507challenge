from mcdreforged.api.all import PluginServerInterface, SimpleCommandBuilder, CommandSource, Integer
from random import randrange, random
import time
import threading

PLUGIN_METADATA = {
    'id': 'challenge507',
    'version': '1.0.0',
    'name': 'The 507 Challenge',
    "description": "Think you can survive the infinite dimensions? Lets find out!",
    "author": "Liam Gingrich (jlgingrich+minecraft@proton.me)",
    "dependencies": {
        "mcdreforged": ">=2.0.0-alpha.1"
    }
}

CONFIG = {
    "minimum_delay": 60,  # The minimum number of seconds before a new cycle can begin
    "maximum_delay": 120,  # The maximum number of seconds after which a new cycle can begin
    "warning_time": 30,  # The number of seconds remaining when a vague warning is announced
    "countdown_time": 5,
    # The number of seconds remaining when a second-by-second countdown starts
    "warning_message": "You feel a strange pull..."
}


def get_rand_teleport_command():
    if random() < 0.1:
        return "execute as @a in minecraft:overworld run tp ~ ~ ~"
    elif random() < 0.1:
        return "execute as @a in minecraft:the_nether run tp ~ ~ ~"
    else:
        return "execute as @a run warp " + str(randrange(1, 2147483647))


def warp(cmdsrc: CommandSource):
    server = cmdsrc.get_server()
    server.execute(get_rand_teleport_command())


def conditional_plural(string: str, number: int, invert = False):
    return string + ("" if ((number == 1) ^ invert) else "s")


EVENT_CLOCK = randrange(
    CONFIG["minimum_delay"], CONFIG["maximum_delay"])


def get_clock(cmdsrc: CommandSource):
    server = cmdsrc.get_server()
    global EVENT_CLOCK
    server.broadcast(
        f'Clock is at {EVENT_CLOCK} {conditional_plural("second", EVENT_CLOCK)}')


def set_clock(cmdsrc: CommandSource, ctxt: dict):
    server = cmdsrc.get_server()
    global EVENT_CLOCK
    EVENT_CLOCK = ctxt["new_clock"]
    server.broadcast(
        f'Set clock to {EVENT_CLOCK} {conditional_plural("second", EVENT_CLOCK)}')


def warn_players(server: PluginServerInterface, message: str):
    server.execute(
        'title @a actionbar {"text":"' + message + '","italic":true}')


def clock_cycle(server: PluginServerInterface):
    global EVENT_CLOCK
    while True:
        if EVENT_CLOCK == CONFIG["warning_time"]:
            warn_players(server, CONFIG["warning_message"])

        if EVENT_CLOCK <= CONFIG["countdown_time"]:
            warn_players(
                server, f'{EVENT_CLOCK} {conditional_plural("second", EVENT_CLOCK)} {conditional_plural("remain", EVENT_CLOCK, True)}...')

        if EVENT_CLOCK <= 1:
            server.execute(get_rand_teleport_command())
            EVENT_CLOCK = randrange(
                CONFIG["minimum_delay"], CONFIG["maximum_delay"])
        else:
            EVENT_CLOCK -= 1
            time.sleep(1)


def on_load(server: PluginServerInterface, prev_module: PluginServerInterface):
    builder = SimpleCommandBuilder()
    builder.command('!!warp', warp)
    builder.command('!!clock get', get_clock)
    builder.command('!!clock set <new_clock>', set_clock)
    builder.arg('new_clock', Integer)
    builder.register(server)

    global TIMEKEEPER_THREAD
    TIMEKEEPER_THREAD = threading.Thread(
        target=clock_cycle, args=(server,), name="507 Challenge")


def on_server_startup(server: PluginServerInterface):
    TIMEKEEPER_THREAD.start()
