[app]

# (str) Title of your application
title = Flappy Bird

# (str) Package name
package.name = flappybird

# (str) Package domain (needed for android/ios packaging)
package.domain = org.TheSRavager

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,jpg,kv,atlas,ttf,ogg,wav,mp3

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
source.exclude_dirs = tests, bin, venv, .buildozer, .github

# (str) Application versioning
version = 0.1

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,charset-normalizer==3.3.2

# (str) Icon of the application
icon.filename = %(source.dir)s/IMG_20260730_164421.jpg

# (str) Supported orientation (landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1


[android]

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (int) overrides automatic android.ndk determination when set (integer)
#android.ndk_api = 21

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) The format used to package the app for release mode (aab or apk).
android.release_artifact = apk
