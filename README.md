# FIE Extensions Path Extractor

This is an extension for NVidia Omniverse.

It's a kludge, useful for some development tasks.

It's simple.  It spawns a window with some buttons.  Those buttons will allow a developer running an "Kit" based
application to save a text file containing paths to the extensions currently available to the Kit Extesion Manager.

This is useful in getting a python IDE to "see" extensions that are not in the python path by default,
but are added to the python path at the last moment by Kit, when it resovles the configured extensions
fully.

I originally designed it to allow my instance of PyCharm to index python code inside extensions (to allow code-completion
to function.)

There are buttons to dump "all" extensions and alternatively "enabled" extensions.

If you relink the app, or if the kit app downloads newer versions of extensions from a repository, the file you dump will be outdated and need to be regenerated.  This is unavoidable.  Kit can and does dynamically manage its extensions based on the given config (.toml or .kit) file every run-time.  And further, since it can use network bound repositories, it's possible a change in network services data, will change your extension paths.  So, when your code-completion breaks, it's probably time to run the extension and generate a new .pth file.

It's worth noting here, that the same is true of the extension paths that NVidia puts inside the .vscode project they generate when creating an extension template (./.vscode/settings.json).  That listing of folders can easily fall out of date.  But NVidia provides no solution to updating that list after the initial template generation.

I recommend dumping "all" extensions rather than "enabled."  For code-completion purposes it's better to index all that's available to the runtime under all configurations, rather than all that's currently configured by the running .toml or .kit file.

My hope is that NVidia will make this extension obsolete by providing better support for code-completion and indexing within Kit, in the long run.

# Usage within an IDE environment

Making a particular python IDE "see" the extensions with this file is beyond the scope of this document.  But some hints on windows:

- Kit has a python.bat in the root.  My app's python.bat calls it:
```
@echo off
SET PYTHONPATH=%PYTHONPATH%;.\python_app_site\
.\app\python.bat %*
```
- I created a directory "python_app_site" in my app.

- if a ".pth" text file, containing paths is found in a python's "site" package directory, it will automatically add those
paths to the python path.  So I dump my .pth file from the extension into that dir.
That alone is not enough.  Because just adding to the PYTHONPATH doesn't qualify the directory as a "site."

- documentation for python's "site" module reveals information about "sitecustomize" and "usercustomize" module
imports which can customize a python instance.  I have a sitecustomize.py file in that dir.  It runs automatically as per the documentation.  And it explicitly re-adds the directory as a "site."  This action is what causes python
to read the .pth text file and use it.

 ```
#get our path
import os
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
app_dir_path = os.path.dirname(dir_path)

#get site module and add our app site
import site
print("adding app site dir: " + dir_path)
site.addsitedir(dir_path)

#try and get kit's site dir run sitecustomize

# kit_site_dir_path = os.path.join(app_dir_path,"app","site")
# if not os.path.exists(kit_site_dir_path):
#     kit_site_dir_path = os.path.join(app_dir_path,"app","kit","site")
# kit_site_dir_customize_path = os.path.join(kit_site_dir_path,"sitecustomize.py")
# if os.path.exists(kit_site_dir_customize_path):
#     print("running kit sitecustomize: " + kit_site_dir_customize_path)
#     exec(open(kit_site_dir_customize_path).read())```
```
- Point the IDE to the app's python.bat as its "main interpreter" or as the interpreter to use to index, or code-complete; and it should be able to index.  It'll see the whole of the omni.* packages found, and the like.  In theory, one could also decide to generate stubs by using the python interpreter directly (hint: WingIDE users).

Note: the above all assume the "linked app" is actually Kit, rather than code or create.  You might need to asjust pathing if you are developing through code or create.  As in: not "./app/python.bat" but rather "./app/kit/python.bat"

# A word on sitecustomize
I really hate using sitecustomize here.  But I also hate even more that Kit uses it.

sitecustomize can only be used once, in any python runtime.  And it is meant for the usage of the "site."  Meaning: it's for configuration management.  Meaning: it should be reserved for sysadmins and dev_ops.  It should NOT be consumed by the application.  The application isn't your sysadmin.  It is meant to be configured by the sysadmin.  NVidia is using a sitecustomize in their Kit python.bat system.  And they really shouldn't.

I in turn, am suggesting that you, a developer (who is a sysadmin usually in your own world) should use it; or a usercustomize.  I think that suggestion is reasonable.  Becasue you are configuring a development environment.

You'll see I commented some code that tries to run NVidia's sitecustomize anyway.  But if you take a look at theirs, you'll see it's redundant.  It's just adding static paths to statically configured extensions.  Mine will find those extensions anyway.  So they're not needed when using this solution.

# License

This software is provided under the New BSD license.  See LICENSE.txt.

Portions of the code-base come from NVidia and are licensed under the Apache 2.0 license or other open source licenses.  e.g. the contents of the ./tools directories.

# Included NVidia documentation
Documentation below is from NVidia's original template project for general usage of extensions.


# Extension Project Template

This project was automatically generated.

- `app` - It is a folder link to the location of your *Omniverse Kit* based app.
- `exts` - It is a folder where you can add new extensions. It was automatically added to extension search path. (Extension Manager -> Gear Icon -> Extension Search Path).

Open this folder using Visual Studio Code. It will suggest you to install few extensions that will make python experience better.

Look for "us.fie.omni.ext.pypathextract" extension in extension manager and enable it. Try applying changes to any python files, it will hot-reload and you can observe results immediately.

Alternatively, you can launch your app from console with this folder added to search path and your extension enabled, e.g.:

```
> app\omni.code.bat --ext-folder exts --enable company.hello.world
```

# App Link Setup

If `app` folder link doesn't exist or broken it can be created again. For better developer experience it is recommended to create a folder link named `app` to the *Omniverse Kit* app installed from *Omniverse Launcher*. Convenience script to use is included.

Run:

```
> link_app.bat
```

If successful you should see `app` folder link in the root of this repo.

If multiple Omniverse apps is installed script will select recommended one. Or you can explicitly pass an app:

```
> link_app.bat --app create
```

You can also just pass a path to create link to:

```
> link_app.bat --path "C:/Users/bob/AppData/Local/ov/pkg/create-2021.3.4"
```


# Sharing Your Extensions

This folder is ready to be pushed to any git repository. Once pushed direct link to a git repository can be added to *Omniverse Kit* extension search paths.

Link might look like this: `git://github.com/[user]/[your_repo].git?branch=main&dir=exts`

Notice `exts` is repo subfolder with extensions. More information can be found in "Git URL as Extension Search Paths" section of developers manual.

To add a link to your *Omniverse Kit* based app go into: Extension Manager -> Gear Icon -> Extension Search Path

