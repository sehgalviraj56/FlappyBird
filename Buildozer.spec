[app]

# (str) Title of your application
title = FlappyBird3D

# (str) Package name
package.name = flappybird3d

# (str) Package domain (needed for android packaging)
package.domain = com.thespookyravager

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (include all extensions used)
source.include_exts = py,png,jpg,jpeg,mp3,wav,json

# (list) Application requirements
# pygame, python3 required
requirements = python3,pygame

# (str) Supported orientation (landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (bool) Accept NDK license
android.accept_sdk_license = True

# (str) The Android arch to build for
android.archs = arm64-v8a, armeabi-v7a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (str) Path to build work dir, if you want to use relative paths, use ./
warn_on_root = 1
