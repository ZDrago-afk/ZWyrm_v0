from rich.console import Console

def show_banner():
    console = Console()
    console.print("""
[bold red]
███████╗██╗    ██╗██╗   ██╗██████╗ ███╗   ███╗
╚══███╔╝██║    ██║╚██╗ ██╔╝██╔══██╗████╗ ████║
  ███╔╝ ██║ █╗ ██║ ╚████╔╝ ██████╔╝██╔████╔██║
 ███╔╝  ██║███╗██║  ╚██╔╝  ██╔══██╗██║╚██╔╝██║
███████╗╚███╔███╔╝   ██║   ██║  ██║██║ ╚═╝ ██║
╚══════╝ ╚══╝╚══╝    ╚═╝   ╚═╝  ╚═╝╚═╝     ╚═╝

ZWyrm — Behavioral Antivirus (Linux)
Red-Team–Informed Defense Engine
[/bold red]
""")
