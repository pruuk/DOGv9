# File contains the commands a normal player would use

from commands.command import MuxCommand

# class CmdGet(default_cmds.CmdGet):
#     """
#     Overriding Get Command in order to force player object to recalculate
#     encumberance every time they get another object.

#     pick up something

#     Usage:
#     get <obj>

#     Picks up an object from your location and puts it in your inventory.
#     """
#     key = 'get'
#     aliases = ['grab']
#     locks = 'cmd:all()'
#     help_category = 'general'
#     lock_storage = 'cmd:all()'

#     def func(self):
#         """Implement the command."""
#         super().func()
#         self.caller.update_encumberance()