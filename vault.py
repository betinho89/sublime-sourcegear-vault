import sublime
import sublime_plugin
import os
import os.path
import re
import sys
import subprocess
import locale

CMD_VAULT = ''
COMMENTSTRING = ''
CURPATH = []
HOST = ''
ISDEBUG = True
PASSWORD = ''
REPOSITORYNAME = ''
SSL = False
USERNAME = ''
VAULT_PATH = ''

class NotFoundError(Exception):
    pass

def set_default_options():
    global HOST
    global ISDEBUG
    global PASSWORD
    global REPOSITORYNAME
    global SSL
    global USERNAME
    global VAULT_PATH

    HOST = get_setting('host', "")
    ISDEBUG = get_setting('isdebug', True)
    PASSWORD = get_setting('password', "")
    REPOSITORYNAME = get_setting('repositoryname', "")
    SSL = get_setting('ssl', False)
    USERNAME = get_setting('username', "")
    VAULT_PATH = get_setting('vault_path', "")
    message = ''

    if not USERNAME:
        message = 'Vault: Username isn\'t configured.'
    elif not PASSWORD:
        message = 'Vault: Password isn\'t configured.'
    elif not HOST:
        message = 'Vault: Host server isn\'t configured.'
    elif not REPOSITORYNAME:
        message = 'Vault: Repository name isn\'t configured.'
    elif not VAULT_PATH:
        message = 'Vault: Path to vaul isn\'t configured.'
    elif "vault.exe" not in VAULT_PATH:
        message = 'Vault: The vault path does not point to the application (vault.exe).'
    elif not os.path.exists(VAULT_PATH):
        message = 'Vault: vault.exe not exists.'
    else:
        return True

    sublime.error_message(message)
    return False

def get_setting(key, default = None):
    settings = sublime.load_settings('vault.sublime-settings')
    os_specific_settings = {}
    if os.name == 'nt':
        os_specific_settings = sublime.load_settings('vault (Windows).sublime-settings')
    elif sys.platform == 'darwin':
        os_specific_settings = sublime.load_settings('vault (OSX).sublime-settings')
    else:
        os_specific_settings = sublime.load_settings('vault (Linux).sublime-settings')

    return os_specific_settings.get(key, settings.get(key, default))

def get_path(self, paths):
    spath = ''
    if len(paths) > 0:
        spath = paths[0]
    elif self.window.active_view() and self.window.active_view().file_name():
        spath = self.window.active_view().file_name()
    elif self.window.folders():
        spath = self.window.folders()[0]
    else:
        sublime.error_message('Vault: Can\'t run here.')
        return False

    spath = os.path.realpath(spath)
    return spath

def get_output(cmd):
    startupinfo = None
    if os.name == 'nt':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    if ISDEBUG:
        print('command: ' + cmd)

    proc = subprocess.Popen(cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        startupinfo=startupinfo)

    output = proc.stdout.read().decode("utf-8")
    output = output.replace('\r\n', '\n')

    if ISDEBUG:
        print('output: \n' + output)

    return output

def get_default_cmd(scommand):
    cmd = VAULT_PATH + \
          " -host \"" + HOST + "\" -user \"" + USERNAME + "\"" + \
          " -password \"" + PASSWORD + "\" -repository \"" + REPOSITORYNAME + "\""

    if SSL:
        cmd += " -ssl"

    return cmd

def get_options_by_command(path, cmd, scommand):
    cmd += " " + scommand

    skey = scommand.lower()
    svalue = ''
    parameters = get_setting(skey, {})
    for index in parameters:
        svalue = parameters[index]
        if not svalue:
            cmd += " " + index
        else:
            if index.find("-") != -1:
                if svalue.find('COMMENTSTRING') != -1:
                    cmd += " " + index + " \"" + COMMENTSTRING + "\""
                else:
                    cmd += " " + index + " \"" + svalue + "\""

    return cmd

def run_my_cmd(path, scommand):
    try:
        cmd = get_default_cmd(scommand)
        cmd = get_options_by_command(path, cmd, scommand)

        cmd += " \"" + path + "\""
        output = get_output(cmd)
        message = ''
        if output.find('error') == -1:
            skey = scommand.lower()
            parameters = get_setting(skey, {})
            show_success = get_setting('show_success', False)

            if skey == "listobjectproperties":
                message = parameters['info']
                keys = parameters['keys']
                for sparam in keys:
                    svalue = output.partition('<' + sparam + '>')[-1].rpartition('</' + sparam + '>')[0];
                    message = message.replace(sparam.upper(), svalue)
            elif show_success:
                message = parameters['success']

            message = message.strip()
            if len(message) > 0:
                message = message.replace('PATH', path)
                if show_success or skey == "listobjectproperties":
                    sublime.message_dialog(message)

            return

        mylist = re.findall(r'<!--(.*?)-->', output)
        if len(mylist) == 0:
            message = output.partition('<exception>')[-1].rpartition('</exception>')[0];
            message = message.strip()

        if len(mylist) == 0:
            if len(message) == 0:
                message = output
        else:
            message = " ".join(mylist)
        sublime.error_message(message)

    except:
        print("Unexpected error({0}): {1}".format(sys.exc_info()[0], sys.exc_info()[1]))

class VaultCommand(sublime_plugin.WindowCommand):
    def run(self, paths=[], parameters=None):
        bcontinue = set_default_options()
        if not bcontinue:
            return
        if not parameters:
            return

        global CMD_VAULT
        CMD_VAULT = parameters['cmd_vault']

        path = get_path(self, paths)
        if not path:
            return

        global CURPATH
        CURPATH = path

        bneedcomment = False
        if 'comment' in parameters:
            bneedcomment = parameters['comment']

        if bneedcomment:
            self.window.show_input_panel('Comment: ', '', self.on_input_comment, None, None)
        else:
            run_my_cmd(path, CMD_VAULT)

    def on_input_comment(self, sinput):
        sinput = sinput.strip()
        if len(sinput) == 0:
            sublime.error_message("Please provide a comment")
            return
        else:
            global COMMENTSTRING

            COMMENTSTRING = sinput
            bcontinue = set_default_options()
            if not bcontinue:
                return

            run_my_cmd(CURPATH, CMD_VAULT)
