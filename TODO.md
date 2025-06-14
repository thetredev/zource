# Source tree layout

Something like this would be the ideal structure and outcome I think:
```tree
.
├── build.zig
├── src
│   ├── modules
│   │   └── v1
│   │       ├── cvars
│   │       │   ├── common.zig
│   │       │   ├── css.zig
│   │       │   └── l4d.zig
│   │       ├── events
│   │       │   ├── common.zig
│   │       │   ├── css.zig
│   │       │   └── l4d.zig
│   │       └── players
│   │           ├── common.zig
│   │           ├── css.zig
│   │           └── l4d.zig
│   ├── plugins
│   │   └── loader.zig
│   └── shim
│       ├── plugin_exports.cpp
│       ├── plugin_shim.cpp
│       └── plugin_shim.h
├── test
│   ├── __init__.py
│   ├── test_cvars.py
│   ├── test_events.py
│   └── test_players.py
└── zource
    ├── __init__.py
    └── v1
        ├── cvars.pyi
        ├── events.pyi
        ├── players.pyi
        └── zource.so
```

# Example usage

```python
"""
This sample plugin counts the amount of player deaths that occurred during a round, and prints a summary on the RoundEnd event. The counter is reset on the following events:
- PluginInit
- LevelChange
- RoundStart
- RoundEnd

The global storage counter is deinitialized on the following events:
- PluginDeinit
"""


# note to self: all of these should be implemented in Zig
from zource.v1.events import Event
#from zource.v1.magic import defer   <--- maybe this is a bad idea, don't know
from zource.v1.players import Player
from zource.v1.plugins import Plugin


# note to self: the `Plugin` instance should be the entrypoint of it all and collect garbage automatically on deinit().
plugin = Plugin("death-counter", "0.1.0", "zource usage example: player death counter")

# note to self: StorageContainer and PluginStorage and Plugin (list of StorageContainer objects) should be implemented in Zig
player_storage = plugin.storage.create(int)


@Event.PlayerSpawn
def player_spawn(event: Event.PlayerSpawn):
    # print(...) -> zource.vX.console.log(...)
    print(f"player.userid: {event.player.userid}")
    print(f"player.dead: {event.player.dead}")
    print(f"player.team: {event.player.team}")

    print(f"player did really actually spawn: {event.player.team > 0 and not event.player.dead}")

@Event.PlayerDeath
def player_death(event: Event.PlayerDeath):
    # event.attacker.health -= 10  <-- somewhat like Source.Python
    print(f"headshot: {event.headshot}")

    # calculates the hash of event.victim
    # every time it's accessed or set
    player_storage[event.victim] += 1


@Event.RoundEnd
@Event.defer(player_storage.reset)
def round_end(_: Event.RoundEnd):
    for victim, count in player_storage.items():
        print(f"Victim {victim.username} died {count} times.")


# listen to multiple events at once:
@Event(Event.PluginInit, Event.LevelChange, Event.RoundStart)
def multiple_events_callback():
    player_storage.reset()


# note to self: the `Plugin` instance should take care of all that automatically
# @Event.PluginDeinit
# def plugin_deinit(event: Event.PluginDeinit):
#     player_storage.deinit()
```
