import re
import subprocess
import platform

regex = r"\[command\](?P<command>.+?)\[/command\]"
pattern = re.compile(regex)

def cmd_filter(text):
    return pattern.findall(text)


def cmd_exec(cmds):
    outputs = [("Host", platform.platform())]
    for cmd in cmds:
        try:
            process = subprocess.Popen(cmd.split(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            out = process.communicate()[0]
            outputs.append((cmd, out.decode('utf-8').strip()))
        except Exception as e:
            outputs.append((cmd, str(e)))
    return outputs

def process_command(text):
    return cmd_exec(cmd_filter(text))

if __name__ == "__main__":
    text = "[command]pwd[/command]"
    cmds = cmd_filter(text)
    print(cmd_exec(cmds))