from mcdreforged.api.all import PluginServerInterface, SimpleCommandBuilder, CommandSource, Integer, new_thread
from random import randrange, random
import time


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
    "warning_message": "You feel a strange pull...",
    "always_show_clock": True,
    "clock_display_objective": "clock_display",
    "clock_display_player": "=",
    "force_overworld": True,
    "force_overworld_chance": 0.1,
    "force_nether": True,
    "force_nether_chance": 0.1,
    "force_library": True,
    "force_library_chance": 0.2
}


def conditional_plural(string: str, number: int, invert=False) -> str:
    return string + ("" if ((number == 1) ^ invert) else "s")


def get_rand_teleport_command() -> str:
    if CONFIG["force_overworld"] and random() < CONFIG["force_overworld_chance"]:
        return "execute as @a in minecraft:overworld run tp ~ ~ ~"
    elif CONFIG["force_nether"] and random() < CONFIG["force_nether_chance"]:
        return "execute as @a in minecraft:the_nether run tp ~ ~ ~"
    elif CONFIG["force_library"] and random() < CONFIG["force_library_chance"]:
        return "execute as @a run warp library"
    else:
        return "execute as @a run warp " + str(randrange(1, 2147483647))


EVENT_CLOCK = CONFIG["maximum_delay"]
STOP_THREADS = False


def warp(cmdsrc: CommandSource) -> None:
    server = cmdsrc.get_server()
    global EVENT_CLOCK
    EVENT_CLOCK = CONFIG["countdown_time"]
    server.broadcast(
        f'Set clock to {EVENT_CLOCK} {conditional_plural("second", EVENT_CLOCK)}')


def get_clock(cmdsrc: CommandSource) -> None:
    server = cmdsrc.get_server()
    global EVENT_CLOCK
    server.broadcast(
        f'Clock is at {EVENT_CLOCK} {conditional_plural("second", EVENT_CLOCK)}')


def set_clock(cmdsrc: CommandSource, ctxt: dict) -> None:
    server = cmdsrc.get_server()
    global EVENT_CLOCK
    EVENT_CLOCK = ctxt["new_clock"]
    server.broadcast(
        f'Set clock to {EVENT_CLOCK} {conditional_plural("second", EVENT_CLOCK)}')


def warn_players(server: PluginServerInterface, message: str) -> None:
    server.execute(
        'title @a actionbar {"text":"' + message + '","italic":true}')


@new_thread
def clock_cycle(server: PluginServerInterface) -> None:
    global EVENT_CLOCK
    global STOP_THREADS
    while True:
        if CONFIG["always_show_clock"]:
            server.execute(
                f'scoreboard players set {CONFIG["clock_display_player"]} {CONFIG["clock_display_objective"]} {EVENT_CLOCK}')
        if STOP_THREADS:
            STOP_THREADS = False
            break
        if EVENT_CLOCK == CONFIG["warning_time"]:
            warn_players(server, CONFIG["warning_message"])
        if 0 < EVENT_CLOCK and EVENT_CLOCK <= CONFIG["countdown_time"]:
            warn_players(
                server, f'{EVENT_CLOCK} {conditional_plural("second", EVENT_CLOCK)} {conditional_plural("remain", EVENT_CLOCK, True)}...')
        if EVENT_CLOCK == 0:
            server.execute(get_rand_teleport_command())
            server.execute(
                "execute as @a at @a run fill ~ ~1 ~ ~ ~ ~ minecraft:air")
            EVENT_CLOCK = randrange(
                CONFIG["minimum_delay"], CONFIG["maximum_delay"])
        EVENT_CLOCK -= 1
        time.sleep(1)
    server.logger.info("Stopping event clock")


def on_load(server: PluginServerInterface, prev_module: PluginServerInterface) -> None:
    builder = SimpleCommandBuilder()
    builder.command('!!clock skip', warp)
    builder.command('!!clock get', get_clock)
    builder.command('!!clock set <new_clock>', set_clock)
    builder.arg('new_clock', Integer)
    builder.register(server)
    if prev_module is not None:
        clock_cycle(server)


def on_unload(server: PluginServerInterface):
    global STOP_THREADS
    STOP_THREADS = True


def on_server_startup(server: PluginServerInterface) -> None:
    clock_cycle(server)
    server.execute(
        f'scoreboard objectives add {CONFIG["clock_display_objective"]} dummy "Seconds Remaining"')
