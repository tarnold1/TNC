import os

DebugPrint=False
	
os.environ["QT_XKB_CONFIG_ROOT"] = "/usr/share/X11/xkb"
if(DebugPrint):print(os.environ["QT_XKB_CONFIG_ROOT"])

os.environ["FONTCONFIG_FILE"] = "/etc/fonts/fonts.conf"
if(DebugPrint):print(os.environ["FONTCONFIG_FILE"])
