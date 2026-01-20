# How To Install
Go to ``Tools > Scripts > Import Python Program From File`` and select the ``krita-export-region-plugin.zip`` that you can download [here](https://github.com/djgaven588/KritaExportRegion/releases/latest/krita-export-region-plugin.zip).

If you do not see the option in ``Tools > Scripts`` to import one, you either have:
- The plugin disabled. Check ``Settings > Configure Krita > Python Plugin Manager`` and ensure ``Python Plugin Importer`` is enabled, and restart.
- Or your installation doesn't have plugins available. For Arch Linux, I had to switch which Krita package I used on the AUR to one with plugins.

# How To Use
Select a part of your image you'd like to export, and either go to ``File > Export Region`` or press the default hotkey of ``Alt+Shift+E`` (make sure there is no conflict by searching that keybind in the ``Settings > Configure Krita > Keyboard Shortcuts`` menu).

# Why?
After searching the internet for what I assumed was a basic functionality of Krita, I downloaded and used a plugin called [Krita Export Region](https://github.com/ollyisonit/krita-export-region), which looked like it'd fit my needs.

For some reason though, the Krita API used *CROPS* the selection to only the visible pixels, turning finely placed pixel art into a mess of image dimensions and positions.

This plugin handles that.

It required effectively rewriting the core of the plugin with a different set of APIs, and had different resulting behavior than the original plugin, so I've put this one here seperately with keyterms that should be easier to run into while searching for a solution to this problem.

Credit to [ollyisonit](https://github.com/ollyisonit) for the original plugin and bones of this. Like it, this is under the MIT license.
