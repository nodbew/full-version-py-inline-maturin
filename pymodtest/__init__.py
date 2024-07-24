import sys

msg = ""
msg += f"attributes: {dir(sys.modules[__name__])}\n"
for attr in dir(sys.modules[__name__]):
    msg += f"{attr}: {getattr(sys.modules[__name__], attr)}\n"
raise Exception(msg)