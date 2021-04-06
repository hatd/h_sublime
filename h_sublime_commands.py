import os
import sublime
import sublime_plugin
import subprocess
import re

class CopyPermalinkCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    file_name = self.view.file_name()
    dir_path = os.path.dirname(file_name)

    kwargs = {}
    kwargs["stdout"] = subprocess.PIPE
    kwargs["cwd"] = dir_path

    top_level_cmd = ["git", "rev-parse", "--show-toplevel"]
    top_level = subprocess.Popen(top_level_cmd, **kwargs).stdout.read().decode("utf-8")[:-1]
    kwargs["cwd"] = top_level

    branch, remote_name = self.check_setting(top_level)

    if branch:
      remote_url = subprocess.Popen(["git", "config", "--get", "remote." + remote_name + ".url"], **kwargs).stdout.read()
      if remote_url:
        current_selection = self.view.sel()[0]
        (row_begin,_) = self.view.rowcol(current_selection.begin())
        (row_end,_) = self.view.rowcol(current_selection.end())
        remote = re.sub("^git@.*:", "https://github.com/", remote_url.decode("utf-8")[:-5])
        permalink = file_name.replace(top_level, remote + "/blob/" + branch)
        permalink = permalink + "#L" + str(row_begin + 1)
        if row_begin != row_end:
          permalink = permalink + "-" + str(row_end + 1)
        sublime.set_clipboard(permalink)
      else:
        sublime.set_clipboard("khong tim thay remote: " + remote_name)

  def check_setting(self, top_level):
    repository = top_level.split("/")[-1]
    try:
      if repository:
        repository_settings = sublime.load_settings("h_sublime.sublime-settings").get("copy_permalink").get(repository)
        if repository_settings:
          return [repository_settings["branch"], repository_settings["remote_name"]]
        else:
          sublime.set_clipboard("48:setting truoc khi su dung tinh nang copy_permalink")
        return [False, False]
      else:
        sublime.set_clipboard("co loi khi parse repository")
        return [False, False]
    except AttributeError:
      sublime.set_clipboard("54:setting truoc khi su dung tinh nang copy_permalink")
      return [False, False]

class UpcaseCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    region = self.view.sel()[0]
    selected = self.view.substr(region)

    self.view.replace(edit, region, selected.upper())

class DowncaseCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    region = self.view.sel()[0]
    selected = self.view.substr(region)

    self.view.replace(edit, region, selected.lower())

class CamelcaseCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    region = self.view.sel()[0]
    selected = self.view.substr(region)

    CamelText = ''.join(word.title() for word in selected.split('_'))

    self.view.replace(edit, region, CamelText)

class SnakecaseCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    region = self.view.sel()[0]
    selected = self.view.substr(region)

    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    snake_text = pattern.sub('_', selected).lower()

    self.view.replace(edit, region, snake_text)
    "aaaa_aaa"
