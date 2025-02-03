# The 507 Challenge

> Think you can survive the infinite dimensions? Lets find out!

This Python script hosts and interfaces with a dedicated server running [Minecraft Java Edition 20w14∞](https://minecraft.fandom.com/wiki/Java_Edition_20w14%E2%88%9E) in order to create a sort of "challenge mode". Much like a certain [507](https://scp-wiki.wikidot.com/scp-507), all players in the server will be randomly transported between dimensions at random intervals. Because this is the "Ultimate Content" April Fools' snapshot, which adds new procedurally generated dimensions that randomize existing elements of the game and several [easter egg dimensions](https://minecraft.fandom.com/wiki/Java_Edition_20w14%E2%88%9E#Easter_egg_dimensions), this can land you just about anywhere.

## Config

Because I got lazy, the config options are embedded in the Python script. They're all self-explanatory and default to what I found to be fun values.

`challenge507.py`
```python
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
```

## Dependencies:
- [mcdreforged >=2.0.0-alpha.1](https://github.com/Fallen-Breath/MCDReforged): Install with `pip install mcdreforged`
- [Minecraft Java Edition 20w14∞](https://minecraft.fandom.com/wiki/Java_Edition_20w14%E2%88%9E) dedicated server `.JAR`. I don't have a link, as this needs to be downloaded via a Minecraft client from Mojang's servers.

## Running

Run `mcdreforged init`, then move `challenge507.py` into the `plugins/` folder and move your `minecraft_server.jar` into the `server/` folder

Edit the `start_command` line in `config.yml` to match the name of your server `.jar`; `start_command: java -Dfile.encoding=UTF-8 -Dstdout.encoding=UTF-8 -Dstderr.encoding=UTF-8 -Xms1G -Xmx2G -jar minecraft_server.jar nogui`

The directory should look like below:

```
my_mcdr_server/
 ├─ config/
 ├─ logs/
 │   └─ MCDR.log
 ├─ plugins/
+│   └─ challenge507.py
 ├─ server/
+│   └─ minecraft_server.jar
 ├─ config.yml
 └─ permission.yml
```

You can now start the server from that directory with `mcdreforged`. Have fun!
