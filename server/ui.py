class UI():
    def __init__(self, size):
        self.terminal_size = size

    def format_msg(self, msg, size, color="", char='=', end="\n"):
        if size == None:
            size = self.terminal_size

        espacos = (size - len(msg)-2) // 2
        
        if size == 0:
            espacos = 0

        colors = {
            "": "",
            "red": '\033[31m',
            "green": '\033[32m',
            "yellow": '\033[33m',
            "reset": '\033[0m'
        }

        return f"{colors[color]}{char*espacos} {msg} {char*espacos}{colors['reset']}{end}"
    
    def Intro(self):
        intro = ""
        intro += self.format_msg("WELLCOME", self.terminal_size)
        intro += self.format_msg("TO THE BEST SERVER EVER", self.terminal_size, "yellow")
        intro += self.format_msg("!!!", self.terminal_size, "green")

        return intro

    # login_evel == 0 -> deslogado
    # login_evel == 1 -> logado usuŕio comum
    # login_evel == 2 -> logado admin
    def Menu(self, level):
        index = 1
        menu = "See what you CAN do:\n\n"

        if level != 1:
            menu += f"{index} - Register\n"
            index += 1
        if level == 0:
            menu += f"{index} - Login\n"
            index += 1
        menu += f"{index} - Show teams\n"
        index += 1
        if level != 0:
            menu += f"{index} - Join team\n"
            index += 1
        if level == 2:
            menu += f"{index} - Start team\n"
            index += 1
            menu += f"{index} - Show online clients\n"
            index += 1
        if level != 0:
            menu += f"{index} - Logout\n"
            index += 1
        menu += f"{index} - Close\n"

        menu += "\nSelect: "

        return menu
    
    def getOption(self, level, option):
        option = option - 1
        menu = [
        ["Register", "Login", "Show teams", "Close"], # User unknow - level = 0
        ["Show teams", "Join team", "Logout", "Close"], # Logged in - level = 1
        ["Register", "Show teams", "Join team", "Start team", "Show online clients", "Logout", "Close"] # Adm - level = 2
        ]

        # Verifica se o level e option estão dentro do tamanho do menu
        # if level < 0 or option < 0 or level >= len(menu) or option >= len(menu[level]):
        #     return "Invalid"
        
        return menu[level][option]