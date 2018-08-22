from discord import User
from ona.context import Context
from typing import NamedTuple, Collection, Mapping


class PermSet(NamedTuple):
    allow_users: Collection[int] = []
    deny_users: Collection[int] = []
    allow_roles: Collection[int] = []
    deny_roles: Collection[int] = []
    deny_everyone: bool = False
    allow_everyone: bool = False

    def has_permissions(self, ctx: Context):
        user_id = ctx.author.id
        roles = [role.id for role in ctx.author.roles]
        if user_id in self.deny_users:
            return False
        if user_id in self.allow_users:
            return True

        if any(role in roles for role in self.deny_roles):
            return False
        if any(role in roles for role in self.allow_roles):
            return True

        if self.deny_everyone:
            return False
        if self.allow_everyone:
            return True
        return None


class CommandPerms(NamedTuple):
    command_name: str
    guild_id: int
    channels: Mapping[str, PermSet] = {}
    guild: PermSet = PermSet()

    def to_dict(self):
        chans = {k: v._asdict() for k, v in self.channels.items()}

        return {
            "command_name": self.command_name,
            "guild_id": self.guild_id,
            "channels": chans
        }

    def has_permissions(self, ctx: Context):
        channel_id = str(ctx.channel.id)
        user_id = ctx.author.id
        role_ids = [role.id for role in ctx.author.roles]
        if channel_id in self.channels:
            chan_ps: PermSet = self.channels[channel_id]
            chan_perms = chan_ps.has_permissions(ctx)
            if isinstance(chan_perms, bool):
                return chan_perms

        return self.guild.has_permissions(ctx)

    def channels_from_dict(d):
        '''Converts the dictionary representation of the channels attribute to PermSet Mapping.'''
        channels = dict()
        if isinstance(d, dict):
            for key, val in d.items():
                try:
                    chan = {
                        k: v
                        for k, v in val.items() if k in PermSet._fields
                    }
                    channels[key] = PermSet(**chan)
                except Exception:
                    pass
        return channels

    @classmethod
    def from_dict(cls, obj: Mapping):
        d = {k: v for k, v in obj if k in cls._fields}
        if "channels" in d:
            d["channels"] = channels_from_dict(d["channels"])
        return cls(**d)


def has_permissions(ctx: Context, perms: CommandPerms) -> bool:
    if ctx.author.id in ctx.bot.devs:
        return True

    channel_perms = ctx.channel.permissions_for(ctx.author)
    if channel_perms.administrator:
        return True

    col = ctx.db["command_permissions"]

    result = col.find_one({
        "command_name": ctx.command.qualified_name,
        "guild_id": ctx.guild.id
    })

    try:
        ps = CommandPerms.from_dict(result)
        return ps.has_permissions(ctx)

    except Exception:
        return False
