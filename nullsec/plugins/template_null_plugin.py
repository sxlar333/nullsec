PLUGIN_INFO = {
    "name": "example",
    "commands": ["example_cmd"],
}


def handle_plugin(args):
    print("[Example Plugin] Running...")
    print(f"Args: {args}")


def example_cmd(args):
    print("[+] Example command executed!")
    print("    This is a sample plugin command.")
