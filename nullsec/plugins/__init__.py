PLUGINS = []


def load_plugins():
    import os, importlib.util, sys

    PLUGINS.clear()
    plugin_dir = os.path.dirname(__file__)

    for filename in os.listdir(plugin_dir):
        if (
            "null_plugin" in filename
            and filename.endswith(".py")
            and filename != "__init__.py"
        ):
            module_name = filename[:-3]
            filepath = os.path.join(plugin_dir, filename)

            spec = importlib.util.spec_from_file_location(module_name, filepath)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                try:
                    spec.loader.exec_module(module)

                    if hasattr(module, "PLUGIN_INFO"):
                        PLUGINS.append(
                            {
                                "name": module.PLUGIN_INFO.get("name", module_name),
                                "commands": module.PLUGIN_INFO.get("commands", []),
                                "handler": getattr(module, "handle_plugin", None),
                            }
                        )
                except Exception as e:
                    pass

    return PLUGINS


def get_plugin_commands():
    return {p["name"]: p for p in PLUGINS}


def call_plugin(name, args):
    for p in PLUGINS:
        if p["name"] == name and p["handler"]:
            p["handler"](args)
            return True
    return False
